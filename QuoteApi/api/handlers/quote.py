from api import app, db, request
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


@app.route('/quotes', methods=["GET"])
def quotes():
    # Возвращаем ВСЕ цитаты
    quotes = QuoteModel.query.all()
    return [quote.to_dict() for quote in quotes]


@app.get('/quotes/<int:quote_id>')
def quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        return quote.to_dict(), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404


@app.get('/authors/<int:author_id>/quotes')
# Возвращаем все цитаты автора
def quote_by_author(author_id):
    author = AuthorModel.query.get(author_id)
    quotes = author.quotes.all()
    return [quote.to_dict() for quote in quotes]
    
    
@app.route('/authors/<int:author_id>/quotes', methods=["POST"])
def create_quote(author_id):
    quote_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404

    quote = QuoteModel(author, quote_data["text"])
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict(), 201


@app.route('/quotes/<int:quote_id>', methods=["PUT"])
def edit_quote(quote_id):
    quote_data = request.json
    quote = QuoteModel.query.get(quote_id)
    if quote:
        quote.text = quote_data["text"]
        db.session.commit()
        return quote.to_dict(), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404

@app.route('/quotes/<int:quote_id>', methods=["DELETE"])
def delete_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote:
        db.session.delete(quote)
        db.session.commit()
        return quote.to_dict(), 200
    return {"Error": f"Quote id={quote_id} not found"}, 404
