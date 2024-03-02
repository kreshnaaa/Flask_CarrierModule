from app import app, db

def create(data):
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)