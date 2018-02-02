import sender, recver

s = sender.HeadPhoneSend(name='sender')
r = recver.HeadPhoneRecv(name='recver')
s.start()
r.start()