import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ClienteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Room")
        
        # --- Configuración de Interfaz ---
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.frame_input = tk.Frame(root)
        self.frame_input.pack(padx=10, pady=5, fill=tk.X)

        self.entry_msg = tk.Entry(self.frame_input)
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry_msg.bind("<Return>", lambda e: self.enviar_mensaje())

        self.btn_enviar = tk.Button(self.frame_input, text="Enviar", command=self.enviar_mensaje)
        self.btn_enviar.pack(side=tk.RIGHT)

        # Protocolo de red
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectar()

    def conectar(self):
        try:
            # Cambia esta IP a la del servidor
            self.sock.connect(("127.0.0.1", 9999)) 
            threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar: {e}")
            self.root.destroy()

    def mostrar_mensaje(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def enviar_mensaje(self):
        msg = self.entry_msg.get()
        if msg:
            try:
                self.sock.send(msg.encode('utf-8'))
                if msg.lower() == "exit":
                    self.root.destroy()
                # Mostramos nuestro propio mensaje en el chat
                # (Opcional, si el servidor no te lo devuelve)
                self.mostrar_mensaje(f"Tú: {msg}")
                self.entry_msg.delete(0, tk.END)
            except:
                self.mostrar_mensaje("❌ Error al enviar mensaje.")

    def recibir_mensajes(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data: break
                self.mostrar_mensaje(data)
            except:
                self.mostrar_mensaje("❌ Conexión perdida.")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteGUI(root)
    root.mainloop()