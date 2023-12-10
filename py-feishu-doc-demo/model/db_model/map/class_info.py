from application import db


class ClassInfo(db.Model):
    __tablename__ = 'class_info'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    fullname = db.Column(db.String(256))
    time = db.Column(db.String(64))

    # Relation to Option
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), unique=True)

    def __repr__(self):
        return f"<ClassInfo {self.id} name={self.name} fullname={self.fullname} time={self.time}>"
