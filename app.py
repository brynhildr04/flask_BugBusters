from flask import (Flask, render_template, request, flash, redirect, 
                  url_for, session, jsonify)
from database import DBhandler
import hashlib
import os
import sys
import requests
import base64  # 추가

application = Flask(__name__)
application.config["SECRET_KEY"]="sosohanewhamarket"
application.config['UPLOAD_FOLDER'] = 'static/images'
DB=DBhandler()


# 결제창 관련 (Toss API 활용 by 신우림)
@application.route('/payment', methods=['GET', 'POST'])
@application.route('/payment', methods=['GET', 'POST'])
def process_payment():
    if request.method == 'POST':
        amount = request.form.get('amount')
        order_id = f"order_{hashlib.sha256(str(amount).encode()).hexdigest()[:8]}"
        
        test_api_key = "test_ck_Z1aOwX7K8m4yDoaADg6aryQxzvNP"
        secret_key = test_api_key + ":"
        auth_key = base64.b64encode(secret_key.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "amount": int(amount),
            "orderId": order_id,
            "orderName": "이화마켓 상품 구매",
            "successUrl": request.url_root + "payment_success",
            "failUrl": request.url_root + "payment_fail",
            "cardNumber": "4242424242424242",  # 테스트용 카드번호
            "cardExpirationYear": "24",         # 테스트용 만료연도
            "cardExpirationMonth": "12",        # 테스트용 만료월
            "cardPassword": "12",               # 테스트용 비밀번호
            "customerName": "테스트",
            "customerEmail": "test@example.com"
        }
        
        try:
            response = requests.post(
                "https://api.tosspayments.com/v1/payments/key-in",
                json=payload,
                headers=headers
            )
            print(response.json())  # 디버깅용
            if response.status_code == 200:
                return redirect(response.json()['paymentUrl'])
            return f"결제 초기화 실패: {response.json()['message']}", 400
        except Exception as e:
            print(str(e))  # 디버깅용
            return str(e), 400
            
    return render_template('payment.html')

#메인 홈화면
@application.route("/")
def hello():
    return render_template("main_product.html")

#서비스 홈화면
@application.route("/main_service.html")
def view_service():
    return render_template("main_service.html")

#장바구니
@application.route("/cart_product.html")
def view_cart():
    return render_template("cart_product.html")


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

@application.route("/상품등록하기.html")
def view_register():
    return render_template("상품등록하기.html")

# kimjiyoon의 추가 페이지 라우트들
@application.route('/payment.html')
def view_payment():
    return render_template('payment.html')

@application.route('/aboutus.html')
def view_aboutus():
    return render_template('aboutus.html')

@application.route('/chat_product.html')
def view_chat_product():
    return render_template('chat_product.html')

@application.route('/chat_service.html')
def view_chat_service():
    return render_template('chat_service.html')

@application.route('/purchase_service.html')
def view_purchase_service():
    return render_template('purchase_service.html')

@application.route('/purchase_product.html')
def view_purchase_product():
    return render_template('purchase_product.html')

#리뷰 작성 페이지
@application.route("/review.html")
def review_write():
    return render_template("review.html")

#리뷰 상세보기 페이지
@application.route("/review_detail.html")
def view_review_detail():
    return render_template("review_detail.html")

#전체 상품 조회 페이지
@application.route("/all_product.html")
def view_all_products():
    return render_template("all_product.html")

#전체 서비스 조회 페이지
@application.route("/all_service.html")
def view_all_services():
    return render_template("all_service.html")


#회원가입 백엔드 연결
@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!") #중복된 아이디 있으면 플래시 메세지 생성
        return render_template("signup.html") 

#제품등록 백엔드 연결
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data = {
        "title": request.form.get("title", ""),
        "price": request.form.get("price", ""),
        "product_type": request.form.get("product_type", ""),
        "category": request.form.get("category", ""),
        "description": request.form.get("description", "")
    }
    
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            image.save(os.path.join(application.config['UPLOAD_FOLDER'], image.filename))
            img_path = url_for('static', filename='images/' + image.filename)
            
            DB.insert_item(data['title'], data, image.filename)
            return render_template("상품등록결과.html", data=data, img_path=img_path)
    
    return render_template("상품등록결과.html", data=data, img_path=None)

if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)



