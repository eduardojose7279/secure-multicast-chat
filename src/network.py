import socket
import struct
from src.config import MULTICAST_GROUP, PORT, BUFFER_SIZE, TTL


def create_multicast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Permite rodar múltiplos clientes na mesma máquina para testes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    sock.bind(("", PORT))

    # Inscreve o socket no grupo multicast
    mreq = struct.pack(
        "4s4s",
        socket.inet_aton(MULTICAST_GROUP),
        socket.inet_aton("0.0.0.0"),
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

    return sock


def send_message(sock, data: bytes):
    sock.sendto(data, (MULTICAST_GROUP, PORT))


def receive_message(sock):
    data, address = sock.recvfrom(BUFFER_SIZE)
    return data, address
