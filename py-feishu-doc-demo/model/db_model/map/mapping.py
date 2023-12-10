from application import db


class Mapping(db.Model):
    __tablename__ = "mapping"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_name = db.Column(db.String(64), unique=True)
    text = db.Column(db.String(256))
    placeholder = db.Column(db.String(256))
    options = db.relationship('Option', backref='mapping', lazy=True)

    def __repr__(self):
        return f"<Mapping {self.field_name} text={self.text} placeholder={self.placeholder}>"

