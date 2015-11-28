from server import app
from model import db, connect_to_db


connect_to_db(app)

db.drop_all()
db.create_all()
