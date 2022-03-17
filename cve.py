import ipaddress

def main():

    print("Welcome to IRZ haxor shit 0.1")
    print("########")
    print()
    print()

    print("1. Post Authentication RCE (Needs credentials)")
    print("2. CSRF to RCE (No credentials)")
    option = input("Select an option: ")

    select_exploit(option)


def select_exploit(user_option):
    match user_option:
        case "1":
            exploit1()
        case "2":
            exploit2()


# Post Authentication RCE exploit
def exploit1():
    print("Running Post Auth RCE exploit")
    print()
    print()
    router_ip = ipaddress.ip_address(input("Enter the router ip to exploit: "))
    router_port = int(input("Enter the victim router web page port (default is 80): "))

    router_user = input("Enter the username for the router login: ")
    router_pass = input("Enter the password for the router login: ")

    

def exploit2():
    print("sup: ")

main()
