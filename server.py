from flask_app import app
from flask_bootstrap import Bootstrap5
from flask_app.controllers import users,goals



if __name__ == "__main__":
    Bootstrap5(app)
    app.run(debug=True, host="localhost", port=5000)