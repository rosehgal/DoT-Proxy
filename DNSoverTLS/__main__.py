import logging.config

from DNSoverTLS.dns_handler import DNSUDPServer, DNSTCPServer

config = {
  "logger": {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "simple": {
        "format": "%(asctime)s [%(process)s] [%(processName)s] [%(threadName)s] %(levelname)s %(name)s:%(lineno)d - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S"
      }
    },
    "handlers": {
      "console": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "stream": "ext://sys.stdout"
      }
    },
    "loggers": {
      "adal-python": {
        "level": "DEBUG"
      }
    },
    "root": {
      "level": "INFO",
      "handlers": [
        "console"
      ]
    }
  }
}

logging.config.dictConfig(config['logger'])


_log = logging.getLogger(__name__)


def start():
    """
    Start the proxy server.
    """
    _log.info('Starting proxy server ...')
    _log.info('Starting DNS Server ...')

    DNSUDPServer().start_thread()
    DNSTCPServer().start_thread()

    _log.info('Started DNS Server in threaded mode.')


start()
