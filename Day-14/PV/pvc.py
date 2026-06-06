import socket
import os

hostname = socket.gethostname()
curent_dir = os.getcwd()
data = {
"Curent_Folder": curent_dir,
"Host Name": hostname
}
print(data)
