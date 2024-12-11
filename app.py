from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import os
import sys
import math
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import random


application = Flask(__name__)
application.config["SECRET_KEY"]="sosohanewhamarket"
application.config['UPLOAD_FOLDER'] = 'static/images'
DB=DBhandler()

#파이썬으로 이메일을 보내기 위한 코드
    #587포트 및 465포트 존재
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
    #로그인을 통해 지메일 접속
smtp.login('park.sumin2004@gmail.com', 'kdew xhur tlrn hhlg')

#첫화면
@application.route("/")
def hello():
    session['status']="product"
    return render_template("firstpage.html")


#마이페이지
@application.route("/profile.html")
def view_profile():
    data=DB.get_user(session['id'])
    if(data==None):
        return render_template("login.html")
    heart=DB.get_heart_byId(session['id'])
    user_posts = DB.get_posts_by_user(session['id'])
    user_comments = DB.get_comments_by_user(session['id'])
    return render_template("profile.html", data=data, posts=user_posts, 
        comments=user_comments,heart=heart)



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

#이메일 보내기
@application.route("/sendingId", methods=['POST'])
def sendId():        
    email=request.form['email_id']+"@"+request.form['email_domain']
    print(email)
    user=DB.get_user(email)
    if (user==None):
        flash("가입한 적 없는 이메일 입니다.")
        return redirect(url_for('view_find_id'))
    uid=user['id']
    print(uid)
    try: 
        #내용을 입력하는 MIMEText => 다른 라이브러리 사용 가능
        msg = MIMEText(('가입하신 아이디는 %s 입니다.'%uid), "plain")
        msg['Subject'] = '소소한 이화: 아이디 전송 메일입니다'

        #이메일을 보내기 위한 설정(Cc도 가능)
        smtp.sendmail('park.sumin2004@gmail.com', email, msg.as_string())
        #객체 닫기
        smtp.quit()
    except:
        flash("이메일 전송에 실패했습니다. 존재하지 않는 이메일일 수 있습니다.")
        return render_template("/find_id.html")
    flash("가입하신 이메일로 아이디가 전송되었습니다.")
    return render_template("/login.html")

@application.route("/sendingPW", methods=['POST'])
def sendingPW():
    uid=request.form["id"]
    stdNum=request.form['stdNum']
    email=request.form['email_id2']+"@"+request.form['email_domain2']
    user_key=DB.find_user_forPW(uid, stdNum, email)
    if(user_key==None):
        flash("가입한 적 없는 회원정보 입니다.")
        return render_template("/find_id.html")
    temp_pw=str(int(random.random()*1000000))
    pw_hash = hashlib.sha256(temp_pw.encode('utf-8')).hexdigest()
    DB.change_pw(user_key, pw_hash)
    try:  
        #내용을 입력하는 MIMEText
        msg = MIMEText(('새 비밀번호는 %s 입니다.'%temp_pw), "plain")
        msg['Subject'] = '소소한 이화: 임시 비밀번호 전송 메일입니다'
        #이메일을 보내기 위한 설정
        smtp.sendmail('park.sumin2004@gmail.com', email, msg.as_string())
        #객체 닫기
        smtp.quit()
    except:
        flash("이메일 전송에 실패했습니다. 존재하지 않는 이메일일 수 있습니다.")
        return render_template("/find_id.html")
    
    flash("새 비밀번호가 가입하신 이메일로 전송되었습니다.")
    return render_template("/login.html")

#제품 상세 페이지 백엔드 연결
@application.route("/view_detail/<name>/")
def view_product_detail(name):
    data=DB.get_item_byname(str(name))
    DB.update_rate(name)
    DB.update_popularity(name, 1)
    return render_template("detail.html", name=name, data=data)

#상품 등록하기
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

# 게시판 작성 페이지
@application.route('/board_write/<name>/')
def view_board_write(name):
    writer = session.get('id', 'unknown_user')  # 세션에서 안전하게 ID 가져오기
    print(f"Accessing board_write for product: {name}, writer: {writer}")  # 디버깅 메시지
    return render_template('board_write.html', name=name, writer=writer)

# 작성된 게시판 게시글 백엔드로 넘겨주기
@application.route("/post_write", methods=["POST"])
def post_write():
    data = request.form
    user_id = session.get('id', 'unknown_user')  # 세션에서 사용자 ID 가져오기
    print(f"User ID for post_write: {user_id}")  # 디버깅 메시지

    date = f"{datetime.today().year}.{datetime.today().month}.{datetime.today().day}."
    item_name = data.get("name", "unknown_item")  # 상품 이름 가져오기
    item_name, post_key = DB.save_post(data, user_id, date)

    if not post_key:
        return "Failed to save post", 500

    return redirect(url_for("view_board_list", name=item_name))

# 제품에 대한 게시글 리스트 보여주기
@application.route("/board_list/<name>/")
def view_board_list(name):
    posts = DB.get_post_by_name(name)
    updated_posts = []
    
    if not posts:
        posts = {}
        print(f"No posts for {name}, showing empty board.")  # 디버깅 메시지
    return render_template("board_list.html", posts=posts, name=name)

# 각 게시글 상세 페이지 보기
@application.route("/post_detail/<item_name>/<post_key>")
def view_post_detail(item_name, post_key):
    updated_views = DB.increment_views(item_name, post_key)
    post = DB.get_post_by_key(item_name, post_key)

    comments = DB.get_comments_by_post(item_name, post_key)

    if post:
        return render_template("board_view.html", post=post, item_name=item_name, post_key=post_key, comments=comments)
    else:
        return "Post not found", 404

#제품별 게시판 보기
@application.route('/board_view.html')
def view_board_view():
    return render_template('board_view.html')

#게시글 지우기
@application.route("/delete_post/<item_name>/<post_key>", methods=["DELETE"])
def delete_post(item_name, post_key):
    postpassword = request.args.get('password')
    post = DB.get_post_by_key(item_name, post_key)
    print(f"Fetched post: {post}")  # 게시글 데이터를 출력하여 비밀번호 포함 여부 확인
    print(f"Deleting post - Input Password: {postpassword}, Stored Password: {post['psw'] if post else 'No Post Found'}")  # 디버깅 추가
    if post and str(post["psw"]) == str(postpassword):
        DB.delete_post(item_name, post_key)
        return '', 200
    else:
        return '', 401

#게시글 수정하기
@application.route("/board_modify/<item_name>/<post_key>", methods=["GET", "POST"])
def modify_post(item_name, post_key):
    if request.method == "POST":
        postpassword = request.form.get("psw")
        print(f"Received Password: {postpassword}")  # 디버깅 로그 추가
        if not postpassword:
            return "비밀번호가 입력되지 않았습니다.", 400

        post = DB.get_post_by_key(item_name, post_key)

        if not post:
            return "게시글을 찾을 수 없습니다.", 404
        if not post.get("psw"):
            return "게시글에 저장된 비밀번호가 없습니다.", 500
        print(f"Database Password: '{post['psw']}', Input Password: '{postpassword}'")
        if post["psw"] != postpassword:
            return jsonify({"error": "비밀번호가 일치하지 않습니다."}), 401

        new_data = {
            "title": request.form.get("postTitle"),
            "content": request.form.get("postContent"),
        }

        if DB.update_post(item_name, post_key, new_data):
            # 게시글 수정 성공 시 수정된 게시글 상세 페이지로 렌더링
            updated_post = DB.get_post_by_key(item_name, post_key)
            comments = DB.get_comments_by_post(item_name, post_key)
            return render_template(
                "board_view.html",
                post=updated_post,
                item_name=item_name,
                post_key=post_key,
                comments=comments,
            )

        return jsonify({"error": "게시글 업데이트에 실패했습니다."}), 500

    post = DB.get_post_by_key(item_name, post_key)
    return render_template("board_modify.html", post=post, item_name=item_name, post_key=post_key) 

#댓글 작성
@application.route('/comment_write/<item_name>/<post_key>/', methods=["POST"])
def write_comment(item_name, post_key):
    user_id = session.get('id', 'unknown_user')  # 세션에서 사용자 ID 가져오기
    content = request.form.get("commentContent", "")
    comment_password = request.form.get("commentPassword", "")  # 댓글 비밀번호 받기

    # 댓글 비밀번호가 제대로 입력되었는지 확인
    if not comment_password:
        return "댓글 비밀번호를 입력해야 댓글을 작성할 수 있습니다.", 400

    # 댓글 내용이 없으면 오류 반환
    if not content:
        return "댓글 내용을 입력하세요.", 400

    # 댓글을 DB에 저장
    comment_password=hashlib.sha256(comment_password.encode('utf-8')).hexdigest() #비밀번호 해시값으로 저장
    comment_key = DB.save_comment(item_name, post_key, user_id, content, comment_password)
    if not comment_key:
        return "댓글 저장에 실패했습니다.", 500

    # 댓글 작성 후 해당 게시글의 댓글 목록을 반환
    comments = DB.get_comments_by_post(item_name, post_key)
    return jsonify(comments)

# 댓글 수정
@application.route("/comment_modify/<item_name>/<post_key>/<comment_key>", methods=["GET", "POST"])
def modify_comment(item_name, post_key, comment_key):
        password = request.form.get("commentPassword")
        new_content = request.form.get("newContent")

        if not password:
            return "비밀번호가 입력되지 않았습니다.", 400
        if not new_content:
            return "수정할 내용이 입력되지 않았습니다.", 400

        comment = DB.get_comment_by_key(item_name, post_key, comment_key)
        if not comment:
            return "댓글을 찾을 수 없습니다.", 404
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(f"Stored password: {comment['password']}")
        print(f"Hashed input password: {hashed_password}")

        if comment["password"] != hashed_password:
            return "비밀번호가 일치하지 않습니다.", 401

        if DB.update_comment(item_name, post_key, comment_key, new_content):
            return '', 200

        return "댓글 수정에 실패했습니다.", 500


# 댓글 삭제
@application.route("/comment_delete/<item_name>/<post_key>/<comment_key>", methods=["DELETE"])
def delete_comment(item_name, post_key, comment_key):
    comment_password = request.args.get("password")
    comment = DB.get_comment_by_key(item_name, post_key, comment_key)
    hashed_password = hashlib.sha256(comment_password.encode('utf-8')).hexdigest()

    if not comment or comment["password"] != hashed_password:
        return "비밀번호가 일치하지 않습니다.", 401

    if DB.delete_comment(item_name, post_key, comment_key):
        return '', 200
    
    return "댓글 삭제에 실패했습니다.", 500

@application.route('/purchase.html')
def view_purchase_product():
    return render_template('purchase.html')

#지금 상황이 좀 꼬였는데, view_detail에서 바로 review.html로 넘어가버려서 404가 뜨는 중 

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
    DB.update_rate(data['name'])
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
        session['status']="product" #처음 로그인하면 product를 기본으로 설정
        data=DB.get_user(session['id'])
        session['name']=data['name']
        return redirect(url_for('view_main')) #교수님 수업 파일은 상품 리스트가 home 인데 우리는 홈화면이 따로 있으니까... hello()로 고쳐야 할 수도
    else:
        flash("아이디/패스워드가 일치하지 않습니다!")
        return render_template("login.html")

#로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    session['status']="product"
    return redirect("aboutus.html") #교수님 수업 파일은 상품 리스트가 home 인데 우리는 홈화면이 따로 있으니까... hello()로 고쳐야 할 수도

#제품등록 백엔드 연결 #지금 누가 등록했는지에 대한 게 없는데, 만약 추가해야 한다면 로그인이 반드시 필요하다는 것
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data = {
        "seller": session['id'],
        "title": request.form.get("title", ""),
        "price": request.form.get("price", type=int),
        "product_type": request.form.get("product_type", ""),
        "category": request.form.get("category", ""),
        "description": request.form.get("description", ""),
        "rate": 0,
        "rateNum": 0
    }
    
    if 'image' in request.files:
        image = request.files['image']

        if image.filename != '':
            image.save(os.path.join(application.config['UPLOAD_FOLDER'], image.filename))
            img_path = url_for('static', filename='images/' + image.filename)
            
            DB.insert_item(data['title'], data, img_path)
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

    product_type=session['status']
    data=DB.get_items_byproductType(product_type)

    item_counts = len(data) #한 페이지에 start_idx, end_idx 만큼 읽어오기
    item_counts=len(data)
    if item_counts<=per_page:
        data=dict(list(data.items())[:item_counts])
    else:
        data=dict(list(data.items())[start_idx:end_idx])
    tot_count=len(data)
    for i in range(row_count):
        if(i==row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template (
        "/all.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page, #현재 페이지 인덱스
        page_count=int(math.ceil((item_counts/per_page))), #페이지 개수
        total=item_counts
        )
#카테고리별 제품 가져오기
@application.route("/list/<category>")
def view_list_category(category):
    page=request.args.get("page", 0, type=int) #페이지 인덱스 클릭할 때마다 get으로 받아옴
    per_page=8 #한 화면에 상품 8개
    per_row=4 #한 열에는 상품 4개
    row_count=int(per_page/per_row)
    start_idx=per_page*page #page 인덱스로 start_idx, end_idx 생성
    end_idx=per_page*(page+1)

    data=DB.get_items_byCategory(category)

    item_counts = len(data) #한 페이지에 start_idx, end_idx 만큼 읽어오기
    item_counts=len(data)
    if item_counts<=per_page:
        data=dict(list(data.items())[:item_counts])
    else:
        data=dict(list(data.items())[start_idx:end_idx])
    tot_count=len(data)
    for i in range(row_count):
        if(i==row_count-1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template (
        "/all.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page, #현재 페이지 인덱스
        page_count=int(math.ceil((item_counts/per_page))), #페이지 개수
        total=item_counts,
        category=category
        )

#데이터베이스에서 리뷰 가져오기 (전체) 이건 제출용 #이거 조만간 삭제해야 할 거 같은데 금요일에 보여드리고 삭제하든 말든 해야지
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
        page_count=int(math.ceil((item_counts/per_page))),
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
        name=name,
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil((item_counts/per_page))),
        total=item_counts)

#좋아요 기능 백엔드 연결
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})
 
@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    DB.update_popularity(name, 5)
    return jsonify({'msg': '좋아요 완료!'})
@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    DB.update_popularity(name, -5)
    return jsonify({'msg': '안좋아요 완료!'})

#스위치
@application.route('/switch', methods=['GET'])
def show_switch():
    status=session['status']
    return jsonify({'status':status})
@application.route('/toService', methods=['POST'])
def toService():
    status="service"
    session['status']=status
    return jsonify({'msg':'서비스로'})
@application.route('/toProduct', methods=['POST'])
def toProduct():
    status="product"
    session['status']=status
    return jsonify({'msg': '제품으로'})


#검색화면
@application.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # 검색어 가져오기
    data=DB.get_items_byKeyWord(query)
    data = dict(list(data.items())[:])
    total = len(data)  # 검색 결과 개수

    items_per_page = 10  # 한 페이지에 표시할 항목 수
    page_count = (total // items_per_page) + (1 if total % items_per_page > 0 else 0)  # 페이지 수 계산

    return render_template('search.html', query=query, total=total, products=data.items(), page_count=page_count)

#동적 라우팅
@application.route('/dynamicurl/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)


#장바구니 보기
@application.route("/cart.html")
def view_cart():
    cart = DB.get_cart(session['id'])
    if (cart!=None): cart = dict(list(cart.items())[:])
    total=DB.calc_total(session['id'])
    return render_template("cart.html", cart=cart, total_price=total)

# 장바구니에 제품 추가
@application.route("/add_to_cart/<item_name>", methods=['POST'])
def add_to_cart(item_name):
    data={
        "name": item_name,
        "quantity": request.form.get('quantity', "")
    }
    success = DB.add_to_cart(session['id'], data)
    return redirect(url_for('view_cart'))
#장바구니에서 제품 제거
@application.route("/remove_from_cart/<item_name>", methods=['POST'])
def remove_from_cart(item_name):
    DB.remove_item(session['id'], item_name)
    return jsonify({"message": "상품이 장바구니에서 제거되었습니다."})
#장바구니에서 수량 변화
@application.route("/update_cart_quantity/<item_name>", methods=['POST'])
def update_cart_quantity(item_name):
    quantity=request.form.get('quantity')    
    data=DB.update_quantity(session['id'], item_name, quantity)
    total=DB.calc_total(session['id'])
    return jsonify({"message": "수량이 업데이트되었습니다.", "data": data, "total": total})
#장바구니 비우기
@application.route("/clear_cart", methods=['GET'])
def clear_cart():
    DB.clear_cart(session['id'])
    return jsonify({"message": "장바구니가 비워졌습니다."})

# main.html 과 DB연결해보기
@application.route("/main.html")
def view_main():
    product_type = session.get('status', 'product')
    
    # 상품 데이터 가져오기
    data = DB.get_items_byproductType(product_type)
    # 상품이 있는 경우와 없는 경우를 모두 처리
    if data:
        data = dict(list(data.items())[:4])
        print(data)
        return render_template(
            "main.html",
            items_list=data,  # 전체 정렬된 리스트
            total=len(data)    # 전체 개수
        )
    
    # 상품이 없는 경우 기본값 전달
    return render_template(
        "main.html",
        items={},
        items_list=[],
        total=0
    )