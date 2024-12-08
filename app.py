from flask import (Flask, render_template, request, flash, redirect, 
                  url_for, session, jsonify, jsonify)
from database import DBhandler
import hashlib
import os
import sys
from datetime import datetime
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

#제품 상세 페이지 백엔드 연결
@application.route("/view_detail/<name>/")
def view_product_detail(name):
    print("###name: ", name)
    data=DB.get_item_byname(str(name))
    print("###data: ", data)
    return render_template("product_detail.html", name=name, data=data)

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

#지금 상황이 좀 꼬였는데, view_detail에서 바로 review.html로 넘어가버려서 404가 뜨는 중 
@application.route('/question_submit.html')
def view_question_submit():
    return render_template('question_submit.html')

#리뷰 작성 페이지
@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    #로그인 했는지 확인
    if(session.get('id')==None):
        flash("로그인이 필요합니다!")
        return render_template("login.html")
    else:
        return render_template("review.html", name=name)

#작성된 리뷰 백엔드로 넘겨주기
@application.route("/reg_review", methods=['POST'])
def reg_review():
    data=request.form
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    user_id=session.get('id')
    date=str(datetime.today().year)+"."+str(datetime.today().month)+"."+str(datetime.today().day)+"."
    DB.reg_review(data, image_file.filename, user_id, date)
    return redirect(url_for('view_review'))

#리뷰 상세보기 페이지 (전체 페이지 버전)
@application.route("/review_detail/<name>/")
def view_review_detail(name):
    data=DB.get_review_byname(str(name))
    return render_template("review_detail.html", name=name, data=data)

#리뷰 상세보기 페이지 (iframe 버전)
@application.route("/review_detail/<name>/<key>/")
def view_itemReview_detail(name, key):
    data=DB.get_review_bykey(str(name), str(key))
    return render_template("review_detail.html", name=key, data=data)


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

#로그인 백엔드 연결
@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash=hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_, pw_hash):
        session['id']=id_
        return redirect(url_for('view_list')) #교수님 수업 파일은 상품 리스트가 home 인데 우리는 홈화면이 따로 있으니까... hello()로 고쳐야 할 수도
    else:
        flash("아이디/패스워드가 일치하지 않습니다!")
        return render_template("login.html")

#로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list')) #교수님 수업 파일은 상품 리스트가 home 인데 우리는 홈화면이 따로 있으니까... hello()로 고쳐야 할 수도

#제품등록 백엔드 연결 #지금 누가 등록했는지에 대한 게 없는데, 만약 추가해야 한다면 로그인이 반드시 필요하다는 것
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

#데이터베이스에서 등록된 상품 정보 가져오기 (전체)
@application.route("/list")
def view_list():
    page=request.args.get("page", 0, type=int) #페이지 인덱스 클릭할 때마다 get으로 받아옴
    per_page=8 #한 화면에 상품 8개
    per_row=4 #한 열에는 상품 4개
    row_count=int(per_page/per_row)
    start_idx=per_page*page #page 인덱스로 start_idx, end_idx 생성
    end_idx=per_page*(page+1)
    data=DB.get_items()
    item_counts = len(data) #한 페이지에 start_idx, end_idx 만큼 읽어오기
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count=len(data)

    for i in range(row_count):
        if(i==row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template (
        "/all_product.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page, #현재 페이지 인덱스
        page_count=int((item_counts/per_page)+1), #페이지 개수
        total=item_counts
        )

#데이터베이스에서 리뷰 가져오기 (전체) 이건 제출용
@application.route("/all_review")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page=8
    per_row=4
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_reviews() #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else: 
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "/all_review.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

#데이터베이스에서 리뷰 가져오기 (상품별)
@application.route("/<name>/all_item_review")
def view_product_review(name): 
    page = request.args.get("page", 0, type=int)
    per_page=3
    per_row=1
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_review_byItemName(name) #read the table
    if(data==None):
        return render_template(
            "/all_item_review.html",
            total=0
        )
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else: 
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "/all_item_review.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

#좋아요 기능 백엔드 연결
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})
 
@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})
@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '안좋아요 완료!'})


#검색화면
@application.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # 검색어 가져오기
    results = [{'name': query, 'img_path': 'default.jpg'}] if query else []  # 임시 검색 결과
    total = len(results)  # 검색 결과 개수

    items_per_page = 10  # 한 페이지에 표시할 항목 수
    page_count = (total // items_per_page) + (1 if total % items_per_page > 0 else 0)  # 페이지 수 계산

    return render_template('search.html', query=query, total=total, products=results, page_count=page_count)





#동적 라우팅
@application.route('/dynamicurl/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
