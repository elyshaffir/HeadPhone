import threading, socket, wave, pyaudio, time

IP = '89.138.138.201'
PORT = 8081
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = .1
WAVE_OUTPUT_FILENAME = 'rec/file.wav'


class HeadPhoneSend(threading.Thread):

    def record(self):
        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def run(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'connecting'
        sender_socket.connect((IP, PORT))
        print 'connected'
        while True:
            with open(WAVE_OUTPUT_FILENAME, 'rb') as f:
                content = f.read()

            sender_socket.send(content)
            time.sleep(.1)