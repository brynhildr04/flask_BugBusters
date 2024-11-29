from datetime import datetime
import pyrebase
import json
class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    

    def insert_item(self, name, data, img_path): #key:value 형식으로 저장된다
        item_info ={
            "seller": data['seller'],
            "addr": data['addr'],
            "email": data['email'],
            "category": data['category'],
            "card": data['card'],
            "status": data['status'],
            "phone": data['phone'],
            "img_path": img_path
        }
        self.db.child("item").child(name).set(item_info) #db에 등록하는 과정
        print(data,img_path)
        return True
    
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'],
            "name": data['name'],
            "stdNum": data['stdNum'],
            "email_id": data['email_id'],
            "email_domain": data['email_domain'],
            "byear": data['byear'],
            "bmonth": data['bmonth'],
            "bday": data['bday'],
            "pw": pw,
            #"pw_check":  pw,
            "phoneNum": data['phoneNum'],
            "address": data['address'],
            "agreed": data['agreed']
        }
        if self.user_duplicate_check(str(data['id'])): #아이디 중복 체크
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get() #user 노드에 사용자 정보 등록
        print("users###",users.val())
        if str(users.val()) == "None": # first registration 이때는 중복 체크로직 타지 않음
            return True
        else:
            for res in users.each():
                value = res.val()

            if value['id'] == id_string:
                return False
            return True
    
    def find_user(self, id_, pw_):
        users=self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value=res.val()
            if value['id']==id_ and value['pw']==pw_:
                return True
        return False
    
    def get_items(self):
        items=self.db.child("item").get().val()
        return items 
    
    #상품 이름으로 item 테이블에서 정보 가져오기
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
        return target_value
    
    #리뷰작성 화면
    def reg_review(self, data, img_path, user_id, date):
        review_info ={
            "name": data['name'],
            "title": data['title'],
            "rate": data['reviewStar'],
            "review": data['reviewContents'],
            "img_path": img_path,
            "user_id": user_id,
            "date": date
        }  
        self.db.child("item").child(data['name']).child('review').push(review_info)
        self.db.child("review").child(data['name']).set(review_info)
        return True

    def get_reviews(self):
        reviews=self.db.child("review").get().val() #이건 상품 구분 없이 모든 리뷰 가져올 떄 사용하는 코드
        return reviews
    
    #리뷰 이름으로 review 테이블에서 정보 가져오기
    def get_review_byname(self, name):
        reviews = self.db.child("review").get()
        target_value=""
        print("###########",name)
        for res in reviews.each():
            key_value = res.key()
            if key_value == name:
                target_value=res.val()
        return target_value
    
    def get_review_byItemName(self, name):
        reviews=self.db.child("item").child(name).child("review").get().val()
        return reviews

    #리뷰 키값으로 review 테이블에서 정보 가져오기
    def get_review_bykey(self, name, key):
        reviews=self.db.child("item").child(name).child("review").get()
        target_value=""
        for res in reviews.each():
            key_value = res.key()
            if key_value == key:
                target_value=res.val()
        return target_value
    
    #좋아요 한 결과 db에 저장
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value
        
        for res in hearts.each():
            key_value = res.key()
        
            if key_value == name:
                target_value=res.val()
        return target_value
        
    def update_heart(self, user_id, isHeart, item):
        heart_info ={
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    
    #질문 등록 밑 데이터 가져오기
    # 질문 목록 가져오기
    def get_qa_posts(self):
        try:
            return self.db.child("qaPosts").get().val()
        except Exception as e:
            print("Firebase에서 질문 목록을 가져오는 중 오류 발생:", e)
            return None

    # 질문 추가
    def add_qa_post(self, title, content, post_type="question"):
        try:
            post_id = self.db.child("qaPosts").push({
                "title": title,
                "content": content,
                "type": post_type,
                "createdAt": datetime.datetime.now().isoformat()
            })["name"]  # Firebase에서 생성된 고유 ID 반환
            return post_id
        except Exception as e:
            print("Firebase에 질문 저장 중 오류 발생:", e)
            return None

    # 특정 질문 가져오기
    def get_post_by_id(self, post_id):
        try:
            post = self.db.child("qaPosts").child(post_id).get().val()
            return post
        except Exception as e:
            print(f"Firebase에서 ID {post_id}의 질문을 가져오는 중 오류 발생:", e)
            return None

    # 모든 질문 가져오기
    def get_all_posts(self):
        try:
            posts = self.db.child("qaPosts").get().val()
            if posts:
                # Firebase 데이터는 사전 형태로 반환되므로, 리스트로 변환
                return [{"id": key, **value} for key, value in posts.items()]
            return []
        except Exception as e:
            print("Firebase에서 모든 질문을 가져오는 중 오류 발생:", e)
            return []

