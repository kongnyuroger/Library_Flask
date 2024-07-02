from flask import render_template, request

def register_routes(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')
