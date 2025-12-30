import pyaudio
import queue
import sys
import audioop

class MicrophoneStream:
    def __init__(self, rate=16000, chunk=8000, threshold=500):
        self.rate = rate
        self.chunk = chunk
        self.buff = queue.Queue()
        self.closed = True
        self.audio_interface = None
        self.stream = None
        self.threshold = threshold

    def __enter__(self):
        self.closed = False
        self.audio_interface = pyaudio.PyAudio()
        self.stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._fill_buffer,
        )
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True
        self.stream.stop_stream()
        self.stream.close()
        self.audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self.buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self.buff.get()
            if chunk is None:
                return
            
            # Noise Gate: Check RMS energy
            # 2 bytes width for paInt16
            rms = audioop.rms(chunk, 2)
            if rms < self.threshold:
                # If too quiet, substitute with silence
                chunk = b'\x00' * len(chunk)
            
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        return
                    
                    # Apply noise gate to buffered chunks too
                    rms = audioop.rms(chunk, 2)
                    if rms < self.threshold:
                        chunk = b'\x00' * len(chunk)
                        
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
