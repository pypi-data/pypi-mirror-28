import logging

from izaber.startup import initializer, request_initialize
from izaber.zconfig import config

class Logger(object):

    _logger = None

    def __call__(self,*args,**kwargs):
        self.info(*args,**kwargs)

    def __getattr__(self,k):
        if not self._logger:
            self._logger = logging.getLogger('main')
        return getattr(self._logger,k)

log = Logger()

@initializer('logging')
def initialize(**kwargs):
    request_initialize('config',**kwargs)
    logging_config = config.get('logging',{})
    logging_config.update( kwargs.get('logging',{}) )

    logging_config.setdefault('filename','/tmp/log.log')
    logging_config.setdefault('filemode','a')
    logging_config.setdefault(
        'format',
        '%(levelname)s %(asctime)s %(module)s: %(message)s'
    )
    logging_config.setdefault('datefmt','%Y-%m-%d %H:%M:%S')
    logging_config.setdefault('level',logging.WARNING)

    logging.basicConfig(**logging_config)

if __name__ == '__main__':
    import izaber.startup
    izaber.startup.initialize()
