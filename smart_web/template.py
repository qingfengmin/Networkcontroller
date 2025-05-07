from flask import render_template

def html_routes(app):
    @app.route('/index.html')
    def index():
        return render_template('index.html')
    
    @app.route('/register.html')
    def register():
        return render_template('register.html')
    
    @app.route('/login.html')
    def login():
        return render_template('login.html')
    
    @app.route('/reset_password')
    def reset_password():
        return render_template('reset_password.html')
    
    @app.route('/config.html')
    def config():
        return render_template('config.html')
    
    @app.route('/device_management.html')
    def device_management():
        return render_template('device_management.html')
    
    @app.route('/first.html')
    def first():
        return render_template('first.html')
    
    @app.route('/third.html')
    def third():
        return render_template('third.html')
    
    @app.route('/fourth.html')
    def fourth():
        return render_template('fourth.html')

    @app.route('/fifth.html')
    def fifth():
        return render_template('fifth.html')