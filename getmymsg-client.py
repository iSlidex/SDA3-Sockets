import asyncio
import threading
import time
import socket
from hashlib import md5
import base64
import sys,getopt

#DEFAULTS
MAX_ATTEMPTS = 3
HOST_IP = '127.0.0.1'
CLIENT_IP = '127.0.0.1'
HOST_PORT = 19876
USER = 'usuario_1'
CLIENT_UDP_PORT = 19877
# Queria hacer esto mas bonito pero bueno... asi quedo...
# Desde python 3.5 si un envio se ve interrumpido, no genera una excepción si no que vuelve a realizar otro envio.

def main(argv):
    # Definiendo los argumentos:
    host_ip, host_port, client_ip, client_udp_port, user = '', '', '', '', ''
    try:
        opts, args = getopt.getopt(argv, "h:p:c:u:o:", ["host_ip=", "host_port=", "client_ip=", "client_udp_port=", "user="])
    except getopt.GetoptError:
        print('Falta un parámetro, el modo de ejecutar es el siguiente:')
        print('getmymsg-client.py -h <host_ip> -p <host_port> -c <client_ip> -u <client_udp_port> -o <user>')
        sys.exit(2)

    # Asignamos los argumentos a las variables locales.
    for opt, arg in opts:
        if opt in ("-h", "--host_ip"):
            host_ip = arg
        elif opt in ("-p", "--host_port"):
            host_port = int(arg)
        elif opt in ("-c", "--client_ip"):
            client_ip = arg
        elif opt in ("-u", "--client_udp_port"):
            client_udp_port = int(arg)
        elif opt in ("-o", "--user"):
            user = str(arg)

    # Si falta algun argumento le asignamos el valor por defecto a la variable local.
    for index,param in enumerate([host_ip, host_port, client_ip, client_udp_port, user]):
        if param == '':
            if index == 0:
                host_ip = HOST_IP
            elif index == 1:
                host_port = HOST_PORT
            elif index == 2:
                client_ip = CLIENT_IP
            elif index == 3:
                client_udp_port = CLIENT_UDP_PORT
            elif index == 4:
                user = USER
    # Ultimo chequeo (No tiene mucho sentido?)
    if '' in (host_ip, host_port, client_ip, client_udp_port, user):
        print('Falta un parámetro')
        sys.exit(2)

    # Abrimos el socket, con with se maneja el caso de cerrarlo, pero por si acaso se cierra mas abajo.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        ATTEMPS = MAX_ATTEMPTS
        while ATTEMPS > 0:
            ATTEMPS -= ATTEMPS
            try:
                s.connect((host_ip, host_port))
                s.send(b''.join([b'helloiam ', bytes(user, 'utf-8 '), b'\n']))
            except socket.timeout:
                print(f'No se pudo enviar el mensaje, volviendo a intentar ({ATTEMPS}/{MAX_ATTEMPTS})')
            else:
                break

        print('Mensaje enviado: '+'helloiam '+str(user))
        ATTEMPS = MAX_ATTEMPTS
        while ATTEMPS > 0:
            ATTEMPS -= ATTEMPS
            try:
                msg = s.recv(64)
            except socket.timeout:
                print(f'No se pudo recibir el mensaje, volviendo a intentar ({ATTEMPS}/{MAX_ATTEMPTS})')
            else:
                break

        print('Mensaje recibido: ' + msg.decode('utf-8'))
        if msg == b'ok\n':
            s.send(b'msglen\n')
            print('Mensaje enviado: msglen' )
            response, msglen = s.recv(1024).decode('utf-8').split()
            print('Mensaje recibido: ' + response+' ' + msglen)
            if msglen.isnumeric():
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
                    udp.bind((client_ip, client_udp_port))
                    print('Escuchando: protocolo UDP IP: '+str(client_ip) + ' Puerto: '+str(client_udp_port))
                    count = MAX_ATTEMPTS
                    while count > 0:
                        try:
                            s.send(b''.join([b'givememsg ', bytes(str(client_udp_port), 'utf-8'), b'\n']))
                            print('Mensaje enviado: givememsg ' + str(client_udp_port))
                            data, addr = udp.recvfrom((int(msglen))*2)
                            count = count - 1
                            if data:
                                print(data)
                                proc_data = (base64.b64decode(data)).decode('utf-8')
                                print('Mensaje recibido: ' + proc_data)
                                md5meker = md5()
                                md5meker.update(proc_data.encode('utf-8'))
                                print('Mensaje enviado: chkmsg '+md5meker.hexdigest())
                                s.send(b''.join([b'chkmsg ', bytes(md5meker.hexdigest(), 'utf-8'), b'\n']))
                                md5check = s.recv(1024)
                                if md5check == b'ok\n':
                                    print('Mensaje recibido: OK ')
                                    s.send(b'bye\n')
                                    time.sleep(2)
                                    print('Mensaje enviado: bye')
                                    s.close()
                                    udp.close()
                                else:
                                    print('Error en checksum')
                                break
                        except socket.timeout:
                            print(f'Problema al recibir... volviendo a intentar, intentos restantes{count}')

        print('FIN')


if __name__ == '__main__':
    main(sys.argv[1:])


