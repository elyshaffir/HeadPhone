import threading, socket, pyaudio, wave

OTHER_IP = '127.0.0.1'
OTHER_PORT_RECV = 8080  # When testing with 2 machines, the other machine should flip the ports when using.
OTHER_PORT_SEND = 8081

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = 'rec/file.wav'


class Recv(threading.Thread):

    def play_recved(self):

        # define stream chunk
        chunk = 1024

        # open a wav format music
        f = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)

        # play stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()


    def run(self):
        recver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recver_socket.bind(('', OTHER_PORT_RECV))
        recver_socket.listen(1)
        r_socket, client_address = recver_socket.accept()
        while True:
            data = ''
            while data[-4:] != 'fuck':
                data += r_socket.recv(1)

            frames = data.split('()()()()()')

            # with open('rec/fuck.wav', 'wb') as f:
                # f.write(data[:-4])
            audio = pyaudio.PyAudio()
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            self.play_recved()


class Sender(threading.Thread):

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

        return '()()()()()'.join(frames)

    def run(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect((OTHER_IP, OTHER_PORT_RECV))
        while True:
            sender_socket.send(self.record() + 'fuck')