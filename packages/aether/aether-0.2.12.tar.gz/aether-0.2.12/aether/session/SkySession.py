from aether.Sky import Sky
from aether.session.GlobalConfig import GlobalConfig

class SkySession(object):

    def GlobalConfig(self):
        return GlobalConfig._getInstance()

    def aether_client(self):
        return GlobalConfig._getInstance()._aether_client()

    def __enter__(self):
        return Sky(self.aether_client())

    def __exit__(self, type, value, traceback):
        pass

