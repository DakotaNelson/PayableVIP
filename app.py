from flask import Flask, render_template
from parse_rest.connection import register

app = Flask(__name__)
app.config.from_object('config')

# register for parse.com
register(app.config['PARSE_APP_ID'],
         app.config['PARSE_API_KEY'],
         master_key=app.config['PARSE_MASTER_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()
