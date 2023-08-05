from sqlalchemy.dialects import registry

registry.register("informix", "sqlalchemy_informix.ibmdb", "InformixDialect")

from sqlalchemy.testing.plugin.pytestplugin import *
