import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ServidorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel de Control - Servidor")
        
        # Lista de clientes y nombres
        self.clientes = []
        self.nombres = {}

        # --- Interfaz ---
        self.log_area = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
        self.log_area.pack(padx=10, pady=10)

        self.entry_msg = tk.Entry(root, width=40)
        self.entry_msg.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry_msg.bind("<Return>", lambda e: self.enviar_anuncio())

        self.btn_enviar = tk.Button(root, text="Anunciar", command=self.enviar_anuncio)
        self.btn_enviar.pack(side=tk.LEFT, pady=10)

        # Iniciar socket
        self.iniciar_red()

    def escribir_log(self, texto):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, texto + "\n")
        self.log_area.config(state='disabled')
        self.log_area.yview(tk.END)

    def difundir(self, mensaje, cliente_remitente=None):
        for cliente in self.clientes:
            if cliente != cliente_remitente:
                try:
                    cliente.send(mensaje.encode('utf-8'))
                except:
                    self.remover_cliente(cliente)

    def enviar_anuncio(self):
        msg = self.entry_msg.get()
        if msg:
            formato = f"🖥️ [SERVER]: {msg}"
            self.difundir(formato)
            self.escribir_log(formato)
            self.entry_msg.delete(0, tk.END)

    def remover_cliente(self, cliente):
        if cliente in self.clientes:
            nombre = self.nombres.get(cliente, "Alguien")
            self.clientes.remove(cliente)
            if cliente in self.nombres:
                del self.nombres[cliente]
            self.difundir(f"📢 {nombre} ha salido del chat.")
            self.escribir_log(f"❌ {nombre} desconectado.")

    def manejar_cliente(self, sc, addr):
        try:
            sc.send("BIENVENIDO. Por favor, ingresa tu nombre: ".encode('utf-8'))
            nombre = sc.recv(1024).decode('utf-8').strip()
            self.nombres[sc] = nombre
            self.clientes.append(sc)
            
            self.escribir_log(f"✅ {nombre} conectado desde {addr}")
            self.difundir(f"📢 {nombre} se ha unido al chat!", sc)
            
            while True:
                recibido = sc.recv(1024)
                if not recibido: break
                mensaje = recibido.decode('utf-8').strip()
                if mensaje.lower() == "exit": break
                
                formato = f"{nombre}: {mensaje}"
                self.escribir_log(formato)
                self.difundir(formato, sc)
        except:
            pass
        finally:
            self.remover_cliente(sc)
            sc.close()

    def aceptar_conexiones(self):
        while True:
            sc, addr = self.server_socket.accept()
            threading.Thread(target=self.manejar_cliente, args=(sc, addr), daemon=True).start()

    def iniciar_red(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", 9999))
        self.server_socket.listen(10)
        self.escribir_log("🚀 Servidor iniciado en puerto 9999")
        threading.Thread(target=self.aceptar_conexiones, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServidorGUI(root)
    root.mainloop()