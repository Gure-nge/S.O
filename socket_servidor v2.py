import socket
import threading

clientes = []
nombres = {}

def difundir(mensaje, cliente_remitente=None):
    """Envía un mensaje a todos los conectados."""
    for cliente in clientes:
        if cliente != cliente_remitente:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                remover_cliente(cliente)

def remover_cliente(cliente):
    if cliente in clientes:
        nombre = nombres.get(cliente, "Alguien")
        clientes.remove(cliente)
        if cliente in nombres:
            del nombres[cliente]
        difundir(f"📢 {nombre} ha salido del chat.")

def manejar_cliente(sc, addr):
    try:
        sc.send("BIENVENIDO. Por favor, ingresa tu nombre: ".encode('utf-8'))
        nombre = sc.recv(1024).decode('utf-8').strip()
        
        nombres[sc] = nombre
        clientes.append(sc)
        
        print(f"✅ {nombre} se unió desde {addr}")
        difundir(f"📢 {nombre} se ha unido al chat!", sc)
        
        while True:
            recibido = sc.recv(1024)
            if not recibido: break
            mensaje = recibido.decode('utf-8').strip()
            if mensaje.lower() == "exit": break
            
            formato = f"{nombre}: {mensaje}"
            print(formato)
            difundir(formato, sc)
            
    except:
        pass
    finally:
        remover_cliente(sc)
        sc.close()

# ✨ NUEVA FUNCIÓN: Permite al servidor escribir en el chat
def consola_servidor():
    while True:
        msg = input("")
        if msg:
            difundir(f"🖥️ [SERVER]: {msg}")
            print(f"🖥️ [SERVER]: {msg}")

def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 9999))
    s.listen(10)
    print("🚀 Servidor iniciado en el puerto 9999")

    # Hilo para que el administrador del servidor hable
    threading.Thread(target=consola_servidor, daemon=True).start()

    while True:
        sc, addr = s.accept()
        threading.Thread(target=manejar_cliente, args=(sc, addr)).start()

if __name__ == "__main__":
    iniciar_servidor()
