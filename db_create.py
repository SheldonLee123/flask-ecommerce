from app import db
from app.models import Category, User

db.create_all()

category = Category(name='Men')
db.session.add(category)
db.session.commit()

category = Category(name='Women')
db.session.add(category)
db.session.commit()

category = Category(name='Gifts')
db.session.add(category)
db.session.commit()
