from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.db'

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flasktutorial'

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysqluser:password@localhost/mysqldb2'

    app.secret_key = 'SOME KEY'


    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('login'))


    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app


#####   @login_manager.user_loader
#####   def load_user(uid):
#####       return User.query.get(uid)

#  ဒီ function က ဘယ်အချိန်မှာ run မလဲ?
#
#  User က login ဝင်ပြီးတိုင်း - page အသစ်တစ်ခုကို သွားတိုင်း
#
#  Request တစ်ခုချင်းစီမှာ - user က logged in ဖြစ်မဖြစ် စစ်ဆေးဖို့
#
#  current_user ကို access လုပ်တိုင်း
#
#  အလုပ်လုပ်ပုံ:
#
#  Flask-Login က session ထဲမှာ user ID ကို သိမ်းထားတယ်
#
#  Page အသစ်တစ်ခုကို သွားတိုင်း ဒီ function ကို ခေါ်ပြီး user ID နဲ့ user object ကို ပြန်ရှာတယ်
#
## ဒါမှ current_user ကို သုံးလို့ရမယ်



#####   @login_manager.unauthorized_handler
#####   def unauthorized_callback():
#####       return redirect(url_for('login'))
#
#  ဒီ function က ဘယ်အချိန်မှာ run မလဲ?
#
#  Login မဝင်ထားတဲ့ user က @login_required route ကို ဝင်ကြည့်တဲ့အခါ
#
## Protected page တွေကို access လုပ်တဲ့အခါ