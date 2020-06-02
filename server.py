import socket
import threading



host = '0.0.0.0'
port = 12345

s = socket.socket()
s.bind((host, port))

print ("Server Started.")
s.listen(5) 
c, addr = s.accept()
print ("client connedted ip:<" + str(addr) + ">")
        


def input_and_send():
        while 1:
            message = input(str("Please enter your command: "))
            c.send(message.encode())
            print("Sent")
            print("")




def Main():
   
    background_thread = threading.Thread(target=input_and_send)
    background_thread.daemon = True
    background_thread.start()


    for message in iter(lambda: c.recv(1024).decode(), ''):
        print(message)
        print("")





    s.close()
    

if __name__ == '__main__':
    Main()
