from flask import render_template,  Blueprint


index = Blueprint("home", __name__)

@index.route("/", methods=['GET'])
def get_rates():
    return render_template("index.html")