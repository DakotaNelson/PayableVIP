from flask import Flask, render_template
from parse_rest.connection import register
from parse_rest.user import User


app = Flask(__name__)
app.config.from_object('config')

# register for parse.com
register(app.config['PARSE_APP_ID'],
         app.config['PARSE_API_KEY'],
         master_key=app.config['PARSE_MASTER_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/')
def test():
    u = User.login("arjun", "password")

    return render_template('test.html', u=u.username)

@app.route('/questions/')
def questions():
    u = User.login("arjun", "password")

    return render_template('questions.html', u=u.username)

@app.route('/dashboard')
def dashboard():
    customers = [{"fname":"Bob"}, {"fname":"Joe"}]
    return render_template('dashboard.html', inStore=customers)

if __name__ == '__main__':
    app.run()
