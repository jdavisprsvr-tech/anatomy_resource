from ..extensions import db


class AnatomyEntry(db.Model):
    __tablename__ = "anatomy_entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    body_system = db.Column(db.String(100), nullable=False)
    is_published = db.Column(db.Boolean, nullable=False, default=False)