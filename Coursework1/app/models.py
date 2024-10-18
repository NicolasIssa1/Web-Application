from app import db

# This will be the database model for the assessments
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(20), nullable=False)
    deadline_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
