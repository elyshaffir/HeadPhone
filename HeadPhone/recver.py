import threading, socket, wave, pyaudio

IP = ''
PORT = 8080
WAVE_OUTPUT_FILENAME = 'rec/file.wav'


class HeadPhoneRecv(threading.Thread):

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
        recver_socket.bind((IP, PORT))
        recver_socket.listen(1)
        r_socket, client_address = recver_socket.accept()

        while True:
            recv = '-'
            content = ''
            while recv != '':
                recv = r_socket.recv(1)
                content += recv

            with open(WAVE_OUTPUT_FILENAME, 'wb') as f:
                f.write(content)
            self.play_recved()
