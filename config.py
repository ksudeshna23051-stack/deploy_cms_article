import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    # Azure Blob Storage
    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'cmsstorage23051'
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or 'n2xcoszTt+GPBTstDbZDaxBhRkobM5g8EfP4mac4khLe+E0OIN3ICKPBpz7cEhBezVe7ySPTrSbj+AStqpxqHA=='
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'images'

    # Azure SQL Database
    SQL_SERVER = os.environ.get('SQL_SERVER') or 'cmsserver23051.database.windows.net'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'cms_db'
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'cmsadmin'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'Cms23051'

    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://' + SQL_USER_NAME + ':' + SQL_PASSWORD + '@' + SQL_SERVER + ':1433/' + SQL_DATABASE + '?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### Microsoft Authentication ###
    CLIENT_SECRET = "LI48Q~9tVusKaSr6L4LavXJCoEpB6UgwY7JLYdbL"

    AUTHORITY = "https://login.microsoftonline.com/common"

    CLIENT_ID = "4357d2a2-3ef8-4811-99b3-07f2f1a44965"

    REDIRECT_PATH = "/getAToken"

    SCOPE = ["User.Read"]

    SESSION_TYPE = "filesystem"
