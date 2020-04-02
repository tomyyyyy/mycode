import pyfiglet

class banner:
    """
        产生一个图标，表示client或者serve
    """
    def __init__(self):
        pass

    def banner(self, ban):
        ascii_banner = pyfiglet.figlet_format(ban)
        print(ascii_banner)
        print("=======================================================")
        print("=======================================================")

    def client_banner(self):
        self.banner("client")

    def serve_banner(self):
        self.banner("serve")
    









