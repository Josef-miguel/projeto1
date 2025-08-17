from flask import Flask

app = Flask(__name__)

# importa as rotas do módulo controllers
from Controllers import routes

if __name__ == "__main__":
    app.run(debug=True)
