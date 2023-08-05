from izaber import config, app_config
from izaber.startup import request_initialize, initializer
from izaber.wamp import wamp

CONFIG_BASE = """
default:
    wamp:
        zerp:
            database: 'databasename'
"""

class ZERPModel(object):
    def __init__(self,zerp,model):
        self.zerp_ = zerp
        self.model_ = model

    def __getattr__(self,k):
        return lambda *a,**k: self.zerp_.call(
            'object.execute',
            self.model_,
            *a, **k
        )

class ZERP(object):
    def __init__(self,*args,**kwargs):
        self.configure(*args,**kwargs)

    def configure(self,
                    wamp=None,
                    database=None):
        if not wamp is None:
            self.wamp = unicode(wamp)
        if not database is None:
            self.database = unicode(database)

    def get_model(self,model):
        return ZERPModel(self,model)

    # Alias
    get = get_model

    def call(self,uri,*args,**kwargs):
        uri = u'.'.join(['zerp',self.database,uri])
        return self.wamp.call(uri,*args,**kwargs)

zerp = ZERP()

@initializer('wamp_zerp')
def load_config(**kwargs):
    request_initialize('wamp',**kwargs)
    config.config_amend_(CONFIG_BASE)
    zerp.configure(wamp,config.wamp.zerp.database)


