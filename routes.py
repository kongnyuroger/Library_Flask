from flask import render_template, request, redirect, url_for, session, send_from_directory, flash
from models import User, Book, Purchase
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import random

def register_routes(app, db, bcrypt,):

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = 'uploads'

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def index():
        return render_template('index.html',)
    
   
    @app.route('/create_book', methods= ['GET', 'POST'])
    def create_book():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            name = request.form['name']
            genre = request.form['genre']
            file = request.files['cover_img']
            description = request.form['description']
            price = request.form['price']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user_id = session['user_id']
                book = Book(name=name, genre=genre, description=description, filename=filename, filepath=filepath, price=price, user_id=user_id)
                db.session.add(book)
                db.session.commit()
                return redirect(url_for('profile'))
            
            return redirect(url_for('create_book'))  # Handle the case where no file is uploaded or file type is not allowed
    
        return render_template('create-book.html' )

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/profile')
    def profile():
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user_id = session['user_id']
            books = Book.query.filter_by(user_id=user_id).all()
            return render_template('profile.html', books=books)
            
    @app.route('/all_books')
    def all_books():
        books = Book.query.all()
        return render_template('all_books.html', books=books )
    
    @app.route('/book/<int:book_id>')
    def book_detail(book_id):
            book = Book.query.get_or_404(book_id)
            if 'user_id' in session:
                user_id = session['user_id']
            else:
                 user_id = None
            return render_template('book_detail.html', book=book, user_id = user_id )
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            user = User.query.filter_by(name=name).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                return redirect(url_for('profile'))
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            file = request.files['profile-pic']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            existing_user = User.query.filter_by(name=name).first()
            if existing_user:
                flash('Username already exists. Please choose a different name.')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user = User(name=name, password=hashed_password, filename=filename, filepath=filepath)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('profile'))
        return render_template('register.html')
    
    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))
    
    @app.route('/buy_book')
    def buy_book():
        return render_template('buy_book.html')
    
    @app.route('/buy_form/<int:id>', methods = ['GET', 'POST'])
    def buy_form(id):
            book = Book.query.get(id)
            user = User.query.get(session['user_id'])
            if request.method == 'POST':
                book = Book.query.get(id)
                name = request.form['name']
                email = request.form['email']
                phone_num = request.form['phone_num']
                user_id = session['user_id']
                book_id = id
                purchase = Purchase(name=name, email=email, phone_num=phone_num, user_id=user_id, book_id=book_id)
                db.session.add(purchase)
                db.session.commit()
                
                return redirect(url_for('buy_book'))
            return render_template('buy_form.html', book=book, user= user)
    
    
    
    @app.route('/delete/<int:id>', methods=['POST'])
    def delete(id):
            book = Book.query.get(id)
            db.session.delete(book)
            db.session.commit()  
            return redirect(url_for('profile'))
    