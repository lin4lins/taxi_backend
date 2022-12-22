from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxi.db'
db = SQLAlchemy(app)
CORS(app)


if __name__ == '__main__':
    app.run(debug=True)
