class Klass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        p = ", ".join(prop for prop in self.__dir__() if not prop.startswith("_"))
        return f"My props are {p}"
