from api import db


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    # default нужен для указани значений поумолчанию, nullable=False(проверка заполнены ил данные), server_default='Ivanov'(все данные у которых небыло указано ранее этого параметра), всегда str
    surname = db.Column(db.String(32), default="Ivanov", nullable=False,
                        server_default="Ivanov")
    quotes = db.relationship('QuoteModel', backref='author', cascade="all,delete", lazy='dynamic')

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name
    #     }
