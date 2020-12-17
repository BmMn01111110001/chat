#!/usr/bin/python3

# серверийг дотоод болон гадаад сүлжээгээр эхлүүлэх сервер скрипт

# Тэмдэглэл: IP хаяг болон портыг хэрэглэгч(client) талтай хуваалцаж чатыг эхлүүлнэ.


import socket, getpass
import sys, os
from os import system, path
from time import sleep
from platform import system as systemos, architecture
from xtwine import Twine


# гадаад сүлжээний холболтыг дамжуулахын тулд servo.net ашиглана
def runServeo():
	print("Гадаад сүлжээнд холбогдож байна....")
	system('ssh -R 9568:0.0.0.0:9568 serveo.net > /dev/null &')
	sleep(5)
	ip = socket.gethostbyname('serveo.net')
	print("IP: {} \t PORT: 9568".format(ip))
	print("Дээрх IP болон PORT дугаарыг client талтай хуваалцна.")

# хэрэглэгчид дотоод сүлжээ эсвэл гадаад сүлжээгээр холбогдох шаардлагатай эсэхийг шалгах
def InternalExternal():
	mode = input("Дотоод эсвэл гадаад сүлжээгээр чатлах уу? (I/E): ")
	if mode.lower() == 'e':
		return True
	elif mode.lower() == 'i':
		return False
	else:
		print("Зөв сонголтыг сонгоно уу!")
		InternalExternal()

def chat(host,port):
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # socket үүсгэх
	server.bind((host, port)) # хост болон портыг холбох
	server.listen(5)
	print("client талаас холбогдохыг хүлээж байна...")
	client, address = server.accept() # client талын холболтыг хүлээн авч баталгаажуулах
	system('clear')
	print('client талтай холбогдлоо : ', address)
	name = input("Таны нэр : ") #  нэр
	keyC = 'sainbnuu>?' # Чатыг шифрлэх, тайлах түлхүүрийг тохируулах
	twine = Twine(key=keyC)
	encrypt = twine.encrypt
	decrypt = twine.decrypt
	while True:
		
		print(decrypt(client.recv(1024))) # хүлээн авсан шифрлэгдсэн msg-ийн шифрийг тайлах
		msg = input("Би : ")
		encMsg = encrypt((name+" : "+msg)).encode() # msg-г шифрлэх
		print('Шифрлэсэн текст: ',encMsg)
		if msg.lower() == "bye":
			client.send(encMsg) # шифрлэгдсэн мсж илгээх
			client.close()
			server.close()
			system("pkill -f 'ssh -R 9568:0.0.0.0:9568 serveo.net'")
			exit(0)
		else:
			client.send(encMsg) # шифрлэгдсэн мсж илгээх

if __name__ == '__main__':
	host = ''
	if InternalExternal():
		runServeo()
		host = "0.0.0.0"
		port = 9568
	else:
		print("local IP/ хост IP-г тохируулах:")
		str(list(str(os.system("hostname -I"))).remove('0'))
		host = input("host оруулна уу: ")
		port = int(input("Port оруулна уу : "))
	try:
		chat(host,port)
	except KeyboardInterrupt:
		print("\nKeyboard Interrupted ! \nBye bye..")
		system("pkill -f 'ssh -R 9568:0.0.0.0:9568 serveo.net'")
		exit()