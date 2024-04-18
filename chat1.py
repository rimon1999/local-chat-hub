import os
import socket
import threading
import tkinter as tk
from datetime import datetime

# Global variables
host = 'localhost'
port_pc1 = 1060
port_pc2 = 1061
payload_size = 2048
conversation_dir = './Conversation'

def receive_messages(sock, text_widget, conversation_file):
    while True:
        try:
            data, _ = sock.recvfrom(payload_size)
            recv_message = data.decode('utf-8')
            text_widget.insert(tk.END, f'\n[PC 2] {recv_message}')
            conversation_file.write(f'[PC 2] {recv_message}\n')
        except Exception as e:
            print("Error receiving message:", e)

def send_message(sock, entry_widget, text_widget, conversation_file):
    message = entry_widget.get()
    if not message:
        return
    text_widget.insert(tk.END, f'\n[PC 1] {message}') 
    conversation_file.write(f'[PC 1] {message}\n')
    sock.sendto(message.encode('utf-8'), (host, port_pc2))

    entry_widget.delete(0, tk.END)

def UDPserver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port_pc1)
    print("PC 1: Starting up echo server on %s port %s" % server_address)
    sock.bind(server_address)

    if not os.path.exists(conversation_dir):
        os.makedirs(conversation_dir)

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    conversation_file_path = os.path.join(conversation_dir, f'conv_{timestamp}.txt')
    conversation_file = open(conversation_file_path, 'w')

    root = tk.Tk()
    root.title("PC 1 Chat")

    text_widget = tk.Text(root)
    text_widget.pack()

    entry_widget = tk.Entry(root)
    entry_widget.pack()

    send_button = tk.Button(root, text="Send", command=lambda: send_message(sock, entry_widget, text_widget, conversation_file))
    send_button.pack()

    receive_thread = threading.Thread(target=receive_messages, args=(sock, text_widget, conversation_file))
    receive_thread.daemon = True
    receive_thread.start()

    root.mainloop()

    print("PC 1: Closing connection")
    sock.close()
    conversation_file.close()

if __name__ == '__main__':
    UDPserver()
