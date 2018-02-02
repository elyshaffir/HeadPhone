import threading


class HeadPhone(threading.Thread):
    def run(self):
        for _ in xrange(10):
            print(threading.current_thread().getName())

x = HeadPhone(name='send')
y = HeadPhone(name='recv')
x.start()
y.start()
