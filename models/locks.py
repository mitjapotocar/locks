from . import db
class Locks(db.Model):
    __tablename__ = 'locks'

    id = db.Column(db.String(100), primary_key=True)
    bridge_id = db.Column(db.String(100), nullable=False)
    bridge_name = db.Column(db.String(255), nullable=False)
    bridge_location = db.Column(db.String(255), nullable=False)
    shared_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending')
    shared_with = db.Column(db.String(100), nullable=True)