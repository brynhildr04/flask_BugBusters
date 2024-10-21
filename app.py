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
    name=request.args.get("name")
    seller=request.args.get("seller")
    addr=request.args.get("addr")
    email=request.args.get("email")
    category=request.args.get("category")
    card=request.args.get("card")
    status=request.args.get("status")
    phone=request.args.get("phone")

    print(name,seller,addr,email,category,card,status,phone)
    return render_template("cart.html")

if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)


