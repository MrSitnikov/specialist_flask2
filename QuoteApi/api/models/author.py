from api import db


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    quotes = db.relationship('QuoteModel', backref='author', cascade="all,delete", lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name
    #     }
