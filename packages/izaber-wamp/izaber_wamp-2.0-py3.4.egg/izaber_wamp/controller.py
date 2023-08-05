from autobahn_sync import AutobahnSync
import os
import certifi

from izaber.compat import *
import wamp

os.environ["SSL_CERT_FILE"] = certifi.where()

class WAMP(object):

    def __init__(self,*args,**kwargs):
        self.wamp = wamp.WAMPClient()
        self.configure(**kwargs)

    def configure(self,**kwargs):
        self.wamp.configure(**kwargs)

    def run(self):
        self.wamp.start()
        return self

    def disconnect(self):
        self.wamp.stop()

    def __getattr__(self,k):
        if not k in (
                        'call',
                        'leave',
                        'publish',
                        'register',
                        'subscribe'
                    ):
            raise AttributeError("'WAMP' object has no attribute '{}'".format(k))
        fn = getattr(self.wamp,k)
        return lambda uri, *a, **kw: fn(
                        uri,
                        *a,
                        **kw
                    )

