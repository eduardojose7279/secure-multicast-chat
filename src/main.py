import threading
from datetime import datetime
from cryptography.exceptions import InvalidTag
from src.network import create_multicast_socket, send_message, receive_message
from src.crypto import derive_key, encrypt_message, decrypt_message


def listen_messages(sock, key: bytes):
    while True:
        try:
            data, address = receive_message(sock)
            message = decrypt_message(data, key)
            print(f"\r{message}\n> ", end="", flush=True)
        except InvalidTag:
            print(
                f"\r[!] Mensagem cifrada de {address[0]} ignorada (chave incorreta)\n> ",
                end="",
                flush=True,
            )
        except OSError:
            break


def main():
    nickname = input("Seu nome: ").strip() or "Anonimo"
    password = input("Chave da sala: ").strip()
    key = derive_key(password)

    sock = create_multicast_socket()

    listener = threading.Thread(
        target=listen_messages, args=(sock, key), daemon=True
    )
    listener.start()

    print("\nConectado ao chat multicast! Digite '/sair' para encerrar.\n")

    try:
        while True:
            text = input("> ").strip()
            if not text:
                continue
            if text.lower() == "/sair":
                break

            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted = f"[{timestamp}] {nickname}: {text}"
            encrypted = encrypt_message(formatted, key)
            send_message(sock, encrypted)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("\nDesconectado.")


if __name__ == "__main__":
    main()
