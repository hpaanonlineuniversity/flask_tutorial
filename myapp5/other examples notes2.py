from flask import Flask, session, make_response, request, render_template, redirect, url_for
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Home page with both session and cookie data
@app.route('/')
def home():
    # Get user info from session
    user_info = {
        'logged_in': session.get('logged_in', False),
        'username': session.get('username'),
        'user_id': session.get('user_id')
    }
    
    # Get preferences from cookies
    preferences = {
        'theme': request.cookies.get('theme', 'light'),
        'language': request.cookies.get('language', 'english'),
        'last_visit': request.cookies.get('last_visit')
    }
    
    # Set last visit cookie
    response = make_response(render_template('home.html', 
                           user=user_info, prefs=preferences))
    response.set_cookie('last_visit', datetime.now().isoformat())
    
    return response

# Login handler
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Simple authentication
    if username and password:  # In real app, check against database
        # Session for user data
        session['user_id'] = 1
        session['username'] = username
        session['logged_in'] = True
        session['login_time'] = datetime.now().isoformat()
        
        # Cookies for preferences
        response = make_response(redirect(url_for('home')))
        response.set_cookie('username', username)  # For display only
        
        # Remember me feature
        if request.form.get('remember_me'):
            # Create secure remember token (in real app, use proper auth token)
            remember_token = secrets.token_urlsafe(32)
            response.set_cookie('remember_token', remember_token, 
                              max_age=30*24*60*60,  # 30 days
                              httponly=True, secure=True)  # Secure flags
        
        return response
    
    return 'Login failed'

# Logout handler
@app.route('/logout')
def logout():
    # Clear session
    session.clear()
    
    # Clear authentication cookies but keep preferences
    response = make_response(redirect(url_for('home')))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('remember_token', '', expires=0)
    
    return response

# Update preferences
@app.route('/update_prefs', methods=['POST'])
def update_preferences():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    
    theme = request.form.get('theme')
    language = request.form.get('language')
    
    # Save some preferences in session
    session['preferences'] = {
        'notifications': request.form.get('notifications', 'off')
    }
    
    # Save UI preferences in cookies
    response = make_response('Preferences updated')
    if theme:
        response.set_cookie('theme', theme, max_age=365*24*60*60)
    if language:
        response.set_cookie('language', language, max_age=365*24*60*60)
    
    return response