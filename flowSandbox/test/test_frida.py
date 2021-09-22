import frida


a = frida.get_device('192.168.1.97:6666').enumerate_processes()

print(a)