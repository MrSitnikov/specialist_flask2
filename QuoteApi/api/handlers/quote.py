from api import app, db, request, multi_auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema,quotes_schema


@app.route('/quotes', methods=["GET"])
def quotes():
    # Возвращаем ВСЕ цитаты
    quotes = QuoteModel.query.all()
    #return [quote.to_dict() for quote in quotes]
    return quotes_schema.dump(quotes)


@app.get('/quotes/<int:quote_id>')
def quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return quote_schema.dump(quote), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404


@app.get('/authors/<int:author_id>/quotes')
# Возвращаем все цитаты автора
def quote_by_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404
    quotes = author.quotes.all()
    return quotes_schema.dump(quotes)
    
# вместо 3-х методом (quote_by_author,quote_by_id,quotes)
# @app.route('/quotes', methods=["GET"])
# @app.route('/quotes/<int:quote_id>', methods=["GET"])
# @app.route('/authors/<int:author_id>/quotes', methods=["GET"])
# def get_quotes(author_id=None, quote_id=None):
#     """
#     Обрабатываем GET запросы
#     :param author_id: id автора
#     :param quote_id: id цитаты
#     :return: http-response(json, статус)
#     """
#     print(f"{author_id=} {quote_id=}")
#     if author_id is None and quote_id is None:  # Если запрос приходит по url: /quotes
#         quotes = QuoteModel.query.all()
#         return [quote.to_dict() for quote in quotes]  # Возвращаем ВСЕ цитаты

#     if author_id:  # Если запрос приходит по url: /authors/<int:author_id>/quotes
#         author = AuthorModel.query.get(author_id)
#         quotes = author.quotes.all()
#         # Возвращаем все цитаты автора
#         return [quote.to_dict() for quote in quotes], 200

#     # Если запрос приходит по url: /quotes/<int:quote_id>
#     quote = QuoteModel.query.get(quote_id)
#     if quote is not None:
#         return quote.to_dict(), 200
#     return {"Error": "Quote not found"}, 404

    
@app.route('/authors/<int:author_id>/quotes', methods=["POST"])
@multi_auth.login_required
def create_quote(author_id):
    quote_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404

    quote = QuoteModel(author, quote_data["text"])
    db.session.add(quote)
    db.session.commit()
    return quote_schema.dump(quote), 201


@app.route('/quotes/<int:quote_id>', methods=["PUT"])
@multi_auth.login_required
def edit_quote(quote_id):
    quote_data = request.json
    quote = QuoteModel.query.get(quote_id)
    if quote:
        for k, v in quote_data.items():
            setattr(quote,k,v)
        #quote.text = quote_data["text"]
        db.session.commit()
        return quote_schema.dump(quote), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404

@app.route('/quotes/<int:quote_id>', methods=["DELETE"])
@multi_auth.login_required
def delete_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return quote_schema.dump(quote), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404
