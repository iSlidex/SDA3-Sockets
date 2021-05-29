## **Actividad #3 para sistemas distribuidos: Trabajemos con sockets.**

Este es un script escrito en python 3.9.5 que realiza conexiones udp y tcp a un servidor dado, se ejecuta utilizando el
interprete de python py, el script espera recibir los siguiente parámetros, si no usará los valores configurados por
defecto.

Variables esperadas: (variable : -argumento_corto, --argumento_largo)

`host_ip : -h , --host_ip=`

`host_port : -p, --host_port=`

`client_ip : -c, --client_ip=`

`client_udp_port : -u, --client_udp_port`

`user : -o, --user`


Valores por defecto:

`HOST_IP = '127.0.0.1'`

`CLIENT_IP = '127.0.0.1'`

`HOST_PORT = 19876`

`USER = 'usuario_1'`

`CLIENT_UDP_PORT = 19877`

Uso (Windows):
```
    En el terminal del windows, cmd o ps ejecutar el siguiente codigo:
    Modelo:
    py getmymsg-client.py -h <host_ip> -p <host_port> -c <client_ip> -u <client_udp_port> -o <user>
    Ejemplo:
    py getmymsg-client.py -h 127.0.0.1 -p 19876 -c 127.0.0.1 -u 19877 -o usuario_1 
```

