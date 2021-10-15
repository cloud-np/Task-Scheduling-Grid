class Network:
    __instance = None
    __network = None

    @staticmethod
    def set_network(network):
        if Network.__instance is None:
            Network()
        Network.__network = network

    @staticmethod
    def get_network() -> float:
        if Network.__instance is None:
            Network()
        return Network.__network

    def __init__(self):
        """ Virtually private constructor. """
        if Network.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Network.__instance = self
