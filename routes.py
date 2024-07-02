from flask import render_template, request

def register_routes(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/create_book')
    def create_book():
        return render_template('create-book.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')
    
    @app.route('/all_books')
    def all_books():
        return render_template('all_books.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')