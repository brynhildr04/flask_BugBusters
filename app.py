from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
application = Flask(__name__)
application.config["SECRET_KEY"]="sosohanewhamarket"
DB=DBhandler()

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

@application.route("/login.html")
def login():
    return render_template("login.html")

@application.route("/signup.html")
def signup():
    return render_template("signup.html")

@application.route("/find_id.html")
def view_find_id():
    return render_template("find_id.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest() #비밀번호는 plaintext로 DB에 저장하면 안됨. 해시를 생성하여 저장.
    if DB.insert_user(data,pw_hash): #아이디 중복체크
        return render_template("login.html")
    else:
        flash("user id already exist!") #중복된 아이디 있으면 플래시 메세지 생성
        return render_template("signup.html") 


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("result.html", data=data, img_path="static/images/{}".format(image_file.filename))
if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)