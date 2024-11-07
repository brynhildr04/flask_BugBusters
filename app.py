from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
application = Flask(__name__)
application.config["SECRET_KEY"]="sosohanewhamarket"
DB=DBhandler()

#메인 홈화면
@application.route("/")
def hello():
    return render_template("review.html")

#서비스 홈화면
@application.route("/main_service.html")
def view_service():
    return render_template("main_service.html")

#장바구니
@application.route("/cart.html")
def view_cart():
    return render_template("cart.html")

#마이페이지
@application.route("/profile.html")
def view_profile():
    return render_template("profile.html")

#로그인
@application.route("/login.html")
def login():
    return render_template("login.html")

#회원가입
@application.route("/signup.html")
def signup():
    return render_template("signup.html")

#아이디/비번 찾기
@application.route("/find_id.html")
def view_find_id():
    return render_template("find_id.html")

#제품 상세 페이지
@application.route("/product_detail.html")
def view_product_detail():
    return render_template("product_detail.html")

#서비스 상세 페이지
@application.route("/service_detail.html")
def view_service_detail():
    return render_template("service_detail.html")

#리뷰 작성 페이지
@application.route("/review.html")
def review_write():
    return render_template("review.html")

#리뷰 상세보기 페이지
@application.route("/review_detail.html")
def view_review_detail():
    return render_template("review_detail.html")

#회원가입 백엔드 연결
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

#제품등록 백엔드 연결
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("result.html", data=data, img_path="static/images/{}".format(image_file.filename))
if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)