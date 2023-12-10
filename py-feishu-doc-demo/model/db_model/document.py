from application import db


class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String)  # combine key
    section = db.Column(db.String)
    relationship = db.Column(db.String)
    document_number = db.Column(db.Integer)  # init
    parent_token = db.Column(db.String(30))
    title = db.Column(db.String(50))  # late init
    token = db.Column(db.String(30))
    obj_token = db.Column(db.String(30))

    def print_doc(self):
        strings = \
            f"[print_code] code: {self.category} {self.section} " \
            f"{self.relationship}{self.document_number:03d} {self.title}" \
            f"token:{self.token} obj_token:{self.obj_token} parent_token:{self.parent_token}"
        print(strings)
        return strings

    def get_codes(self):
        return f"{self.category}{self.section}{self.relationship}{self.document_number:03d}"

    def get_code_title(self):
        return f"{self.get_codes()}{self.title}"

