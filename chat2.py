import socket
import threading
import tkinter as tk

host = 'localhost'
port_pc1 = 1060
port_pc2 = 1061
payload_size = 2048

def receive_messages(sock, text_widget):
    while True:
        try:
            data, _ = sock.recvfrom(payload_size)
            recv_message = data.decode('utf-8')
            text_widget.insert(tk.END, f'\n[PC 1] {recv_message}')
        except Exception as e:
            print("Error receiving message:", e)

def send_message(sock, entry_widget, text_widget):
    message = entry_widget.get()
    if not message:
        return
    text_widget.insert(tk.END, f'\n[PC 2] {message}')  # Display own message
    sock.sendto(message.encode('utf-8'), (host, port_pc1))

    entry_widget.delete(0, tk.END)

def UDPserver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port_pc2)
    print("PC 2: Starting up echo server on %s port %s" % server_address)
    sock.bind(server_address)

    root = tk.Tk()
    root.title("PC 2 Chat")

    text_widget = tk.Text(root)
    text_widget.pack()

    entry_widget = tk.Entry(root)
    entry_widget.pack()

    send_button = tk.Button(root, text="Send", command=lambda: send_message(sock, entry_widget, text_widget))
    send_button.pack()

    receive_thread = threading.Thread(target=receive_messages, args=(sock, text_widget))
    receive_thread.daemon = True
    receive_thread.start()

    root.mainloop()

    print("PC 2: Closing connection")
    sock.close()

if __name__ == '__main__':
    UDPserver()
