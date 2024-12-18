from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3


BASEDIR = Path(__file__).parent.parent


# instanciando Flask
app = Flask(__name__)

# Configurações da app
# Caminho da base de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, 'database/users.db')
app.config["SQLALCHEMY_BINDS"] = {

    "reservations": "sqlite:///" + os.path.join(BASEDIR, 'database/reservations.db'),
    "payment_data": "sqlite:///" + os.path.join(BASEDIR, 'database/payment_data.db')
}

# Secret Key
app.config["SECRET_KEY"] = "abc"

# instanciando base de dados
db = SQLAlchemy()
