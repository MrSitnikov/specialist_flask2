from api import app, db, request,auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.author import author_schema,authors_schema

@app.route('/authors', methods=["GET"])
def get_authors():
    authors = AuthorModel.query.all()
    #authors_dict = [author.to_dict() for author in authors]
    authors_dict = authors_schema.dump(authors)
    return authors_dict, 200


@app.route('/authors/<int:author_id>', methods=["GET"])
def get_author_by_id(author_id):
    author = AuthorModel.query.get(author_id)
    if not author:
        return f"Author id={author_id} not found", 404
    return author_schema.dump(author), 200


@app.route('/authors', methods=["POST"])
@auth.login_required
def create_author():
    author_data = request.json
    author = AuthorModel(**author_data)
    db.session.add(author)
    db.session.commit()
    return author_schema.dump(author), 201


@app.route('/authors/<int:author_id>', methods=["PUT"])
@auth.login_required
def edit_author(author_id):
    author_data = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        return {"Error": f"Author id={author_id} not found"}, 404
    #author.name = author_data["name"]
    for k,v in author_data.items():
        setattr(author,k,v)
    db.session.commit()
    return author_schema.dump(author), 200


@app.route('/authors/<int:author_id>', methods=["Delete"])
@auth.login_required
def delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()
        return author_schema.dump(author), 200
    return {"Error": f"Quote id={author_id} not found"}, 404
