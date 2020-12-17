#!/usr/bin/python3

# сервер рүү холбогдох клиент скрипт
# Тэмдэглэл: серверээс IP болон портын хаягийг авна.

import socket, getpass
from time import sleep
from os import system
from xtwine import Twine


# чатлахдаа сервер рүү холбогдож дараа нь чатлана

def chat(host,port):

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # socket үүсгэх
	system("clear")
	print("сервэртэй холбогдож байна...")
	sleep(5)
	server.connect((host, port))
	print("Сервертэй холбогдлоо {}:{}".format(host,port))
	name = input("Таны нэр : ") 

	keyC = 'sainbnuu>?'

	twine = Twine(key=keyC)
	encrypt = twine.encrypt
	decrypt = twine.decrypt
	while True:
		msg = input("Би : ")
		encMsg = encrypt((name+" : "+msg)).encode() # msg-г шифрлэх
		print('Шифрлэсэн текст: ',encMsg)
		if msg.lower() == "bye":
			server.send(encMsg) # шифрлэгдсэн мсж илгээх
			server.close()
			exit(0)
		else:
			server.send(encMsg) # шифрлэгдсэн мсж илгээх
		print(decrypt(server.recv(1024))) # msg хүлээн авч шифрийг тайлна
if __name__ == '__main__':
	print("Серверийн IP болон PORT шаардлагатай")
	host = input("Серверийн IP хаягийг оруулна уу : ")
	port = int(input("Серверийн портыг оруулна уу : "))
	try:
		chat(host,port)
	except KeyboardInterrupt:
		print("\nKeyboard Interrupted ! \nBye bye...")
		exit()