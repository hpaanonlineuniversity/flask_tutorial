1. User Authentication System
============================================================================================================================================================

from flask import Flask, session, make_response, request, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure secret key

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Authentication check
    if username == 'admin' and password == 'password':
        # Session for sensitive data
        session['user_id'] = 1
        session['username'] = username
        session['logged_in'] = True
        
        # Cookie for preferences/remember me
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('theme', 'dark')  # UI preference
        response.set_cookie('language', 'myanmar')
        
        # Remember me functionality
        if request.form.get('remember_me'):
            response.set_cookie('remember_token', 'some_secure_token', max_age=30*24*60*60)  # 30 days
        
        return response
    return 'Login failed'

@app.route('/dashboard')
def dashboard():
    # Check session for authentication
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get preferences from cookies
    theme = request.cookies.get('theme', 'light')
    language = request.cookies.get('language', 'english')
    
    return f'Dashboard - Theme: {theme}, Language: {language}'



=========================================================================================================================================================

2. Shopping Cart System

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Use session for cart items (secure)
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True  # Ensure session is saved
    
    # Use cookie for cart tracking (analytics)
    response = make_response('Product added to cart')
    response.set_cookie('last_product_viewed', str(product_id))
    response.set_cookie('cart_count', str(len(session['cart'])))
    
    return response

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    last_viewed = request.cookies.get('last_product_viewed')
    
    return f'Cart: {cart_items}, Last Viewed: {last_viewed}'

==============================================================================================================================================================

3. User Preferences System

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    theme = request.form['theme']
    language = request.form['language']
    
    # Sensitive preferences in session
    session['user_preferences'] = {
        'notifications': request.form.get('notifications', 'off')
    }
    
    # UI preferences in cookies
    response = make_response('Preferences saved')
    response.set_cookie('theme', theme, max_age=365*24*60*60)  # 1 year
    response.set_cookie('language', language, max_age=365*24*60*60)
    
    return response

=================================================================================================================



