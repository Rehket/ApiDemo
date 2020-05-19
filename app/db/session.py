from databases import Database
import config


database = Database(config.DATABASE_URI, ssl=config.RDS_SSL_CONTEXT)
