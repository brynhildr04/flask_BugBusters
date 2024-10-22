from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")
@application.route("/home.html")
def view_home():
    return render_template("home.html")
@application.route("/cart.html")
def view_cart():
    return render_template("cart.html")
@application.route("/profile.html")
def view_profile():
    return render_template("profile.html")
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data=request.form
    return render_template("cart.html",data=data)

if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)


