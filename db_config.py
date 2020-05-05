import os 
"""
DB configuration used for the product
"""

# Name of the database
db_name = 'defaultdb'

# DB User to authenticate as
db_user = os.getenv("DB_USER")

# User's password used to connect to DB
db_password = os.getenv("DB_PASSWORD")

# DB host
db_host = os.getenv("DB_HOST")

# DB port
db_port = os.getenv("DB_PORT")
