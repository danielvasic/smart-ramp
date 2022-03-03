from flask_sqlalchemy import SQLAlchemy

MYSQL_CONFIG = {
    "username": "root",
    "password": "Csdigital123.",
    "database": "ramp",
    "server": "212.39.115.105"
}

MYSQL_CONFIG_URI =  "mysql://{}:{}@{}/{}?charset=utf8mb4".format(
    MYSQL_CONFIG["username"], 
    MYSQL_CONFIG["password"],
    MYSQL_CONFIG["server"],
    MYSQL_CONFIG["database"]
)

db = SQLAlchemy()