
import socket
import threading

def connect_client(client_id):
    try:
        s = socket.socket()
        s.connect(('127.0.0.1', 50872))
        msg = f'REGISTER user{client_id} pass{client_id}secret'
        s.sendall(f'LEN:{len(msg)}\n'.encode() + msg.encode())
        resp = s.recv(1024).decode().strip()
        print(f'Client {client_id}: {resp}')
        s.close()
    except Exception as e:
        print(f'Client {client_id} error: {e}')

threads = []
for i in range(1, 11):
    t = threading.Thread(target=connect_client, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n✓ All 10 clients done!")
