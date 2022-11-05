from flask import (
    Blueprint, session, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    if g.user:
        db, c = get_db()
        c.execute(
            "SELECT * FROM books WHERE created_by = %s AND completed = %s",
            (g.user['id'], False)
        )
        books = c.fetchall()
        return render_template("/app/home.html", books=books)
    return render_template('/index.html')

@bp.route('/history')
@login_required
def history():
    db, c = get_db()
    c.execute(
        "SELECT * FROM books WHERE created_by = %s AND completed = %s",
        (g.user['id'], True)
    )
    books = c.fetchall()
    return render_template("/app/history.html", books=books)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("app.index"))

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        book = request.form['book']
        author = request.form['author']
        error = None

        if not book:
            error.append('Book name is required')
        if not author:
            error.append('Author name is required')
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into books (book, author, created_by, completed)'
                ' values (%s, %s, %s, %s)',
                (book, author, g.user['id'], False)
            )
            db.commit()
            return redirect(url_for('app.index'))

    return render_template('app/create.html')

def get_book(id):
    db, c = get_db()
    c.execute(
            "SELECT * FROM books WHERE created_by = %s AND id = %s",
            (g.user['id'], id)
    )

    book = c.fetchone()

    if book is None:
        abort(404, "Book ID {0} doesn't exist".format(id))

    return book

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    book = get_book(id)
    if request.method == "POST":
        bookn = request.form["book"]
        author = request.form["author"]
        completed = True if request.form.get("completed") == "on" else False
        error = None

        if not bookn:
            error.append("Book name is required")
        if not author:
            error.append("Author name is required")
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                    "UPDATE books SET book = %s, author = %s, completed = %s"
                    " WHERE id = %s AND created_by = %s",
                    (bookn, author, completed, id, g.user["id"])
            )
            db.commit()
            return redirect(url_for("app.index"))
    return render_template("app/update.html", book=book)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute('delete from books where id = %s and created_by = %s', (id, g.user['id']))
    db.commit()
    return redirect(url_for('app.index'))
