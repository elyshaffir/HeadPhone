import com

s = com.Sender(name='s')
r = com.Recv(name='r')
s.start()
r.start()