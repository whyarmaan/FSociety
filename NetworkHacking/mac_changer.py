import subprocess

def change_mac(new_mac, interface):
    subprocess.call(f'ifconfig {interface} down', shell=True)
    subprocess.call(f'ifconfig {interface} hw ether {new_mac}', shell=True)
    subprocess.call(f'ifconfig {interface} up', shell=True)

if __name__ == '__main__':
    new_mac, interface = input("[+] Enter New Mac Address('new_mac interfaace'): ").split(" ")
    change_mac(new_mac, interface)
