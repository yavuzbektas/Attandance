import socket,struct

host = "192.168.0.103"
port = 8001

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket oluşturuldu")

    s.bind((host, port))
    print("socket {} nolu porta bağlandı".format(port))

    s.listen(5)
    print("socket dinleniyor")
except socket.error as msg:
    print("Hata:",msg)

while True:

    # Client ile bağlantı kurulursa
    c, addr = s.accept()
    print('Gelen bağlantı:', addr)

    # Bağlanan client tarafına hoşgeldin mesajı gönderelim.
    mesaj = 'on-off'
    data = c.recv(1024)
    data= struct.unpack("f", data)
    c.send(mesaj.encode('utf-8'))
    print(data)
    # Bağlantıyı sonlandıralım
    c.close()