
import os.path
debug = os.path.exists("debug")

import logging
if debug:
	logging.basicConfig(level=logging.DEBUG)
	logging.getLogger('hpack').setLevel(logging.ERROR)
else:
	logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)

from dynamic_config import DynamicConfig
dynamic_config = DynamicConfig()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

engine = create_engine('sqlite:///datebase.db', connect_args={'check_same_thread': False})
sessionmaker = _sessionmaker(bind=engine)

#session = sessionmaker()

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)


if debug:
	_token = dynamic_config.debug_token
else:
	_token = dynamic_config.production_token

from photon import Bot
from context import ContextManager
bot = Bot(_token)
ContextManager(bot)
