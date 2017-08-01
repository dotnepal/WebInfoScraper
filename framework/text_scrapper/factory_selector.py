class SelectorFactory:
    @staticmethod
    def make(selector_name):
        # print selector_name
        if selector_name == "css":
            return "select"
        if selector_name == "xpath":
            return "findall"
        if selector_name== "regex":
            return "regex"