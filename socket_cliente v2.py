import socket
import threading
import sys

def recibir_mensajes(sock):
    """Hilo para recibir datos del servidor constantemente."""
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data: break
            # Borra la línea actual del prompt y muestra el mensaje recibido
            print(f"\r{data}\n> ", end="")
        except:
            print("\n❌ Conexión perdida con el servidor.")
            break

def iniciar_cliente():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Asegúrate de que esta IP sea la correcta de tu servidor
        s.connect(("192.168.0.19", 9999))
    except Exception as e:
        print(f"No se pudo conectar: {e}")
        return

    # Iniciar hilo de recepción
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(s,), daemon=True)
    hilo_recibir.start()

    while True:
        mensaje = input("> ")
        if mensaje.lower() == "exit":
            s.send("exit".encode('utf-8'))
            break
        s.send(mensaje.encode('utf-8'))

    s.close()

if __name__ == "__main__":
    iniciar_cliente()
