from application import db


class Option(db.Model):
    __tablename__ = "option"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    value = db.Column(db.String(64))
    mapping_id = db.Column(db.Integer, db.ForeignKey('mapping.id'))

    # Relation to ClassInfo
    class_info = db.relationship('ClassInfo', backref=db.backref("option", uselist=False), uselist=False)

    def __repr__(self):
        return f"<Option {self.name}={self.value}>"
