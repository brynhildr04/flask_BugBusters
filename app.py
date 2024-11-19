<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 이미지가 저장될 폴더 설정
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    title = request.form['title']
    content = request.form['content']
    rating = request.form['rating']
    image_file = request.files['image']

    # 이미지 파일이 첨부되었는지 확인
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)  # 이미지 파일 저장
        image_url = url_for('static', filename='uploads/' + filename)
    else:
        image_url = None

    # 상품리뷰상세 페이지로 데이터 전달
    return render_template('상품리뷰상세.html', title=title, content=content, rating=rating, image_url=image_url)

@app.route('/write_review')
def write_review():
    return render_template('리뷰작성.html')

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import os
import sys

application = Flask(__name__)
application.config["SECRET_KEY"]="sosohanewhamarket"
application.config['UPLOAD_FOLDER'] = 'static/images'
DB=DBhandler()
@application.route("/cart.html")
def 임시():
    return render_template("cart.html")

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

#제품등록 백엔드 연결
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data = {
        "title": request.form.get("title", ""),
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

#동적 라우팅
@application.route('/dynamicurl/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

if __name__=="__main__":
<<<<<<< HEAD
    application.run(host='0.0.0.0', debug=True)
>>>>>>> 22f38a963d510e12c50383dfbb7886d153b8e70e
=======
    application.run(host='0.0.0.0', debug=True)
>>>>>>> 062c2570a8aac680c9f25efe083314b4d366b997
