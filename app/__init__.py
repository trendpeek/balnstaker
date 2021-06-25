from flask import Flask


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'ec9439cfc6c336ae2029e94s'


from app import routes