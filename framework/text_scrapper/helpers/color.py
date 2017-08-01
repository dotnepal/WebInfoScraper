class Color:
    @staticmethod
    def red(text):
        return "\033[91m{}\033[0m".format(text)

    @staticmethod
    def green(text):
        return "\033[92m{}\033[0m".format(text)

    @staticmethod
    def yellow(text):
        return "\033[93m{}\033[0m".format(text)

    @staticmethod
    def pink(text):
        return "\033[95m{}\033[0m".format(text)

    @staticmethod
    def skyblue(text):
        return "\033[96m{}\033[0m".format(text)
