__version__ = '0.2.2'

import os
from sqlalchemy.dialects import registry

os.environ['DELIMIDENT'] = 'y'

registry.register("informix", "sqlalchemy_informix.ibmdb", "InformixDialect")
