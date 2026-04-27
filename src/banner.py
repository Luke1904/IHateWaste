import pyfiglet

def print_banner():
    version = "v1.1.0"
    # banner text
    banner = pyfiglet.figlet_format("ihatewaste"
    + " " + version, font="slant")
    print("-" * 75)
    print("\033[96m" + banner + "\033[0m")
    print("-" * 75)

if __name__ == "__main__":
    print_banner()
