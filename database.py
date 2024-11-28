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
            "product_type": data['product_type'],
            "category": data['category'],
            "description": data['description'],
            "rate": data['rate'],
            "rateNum": data['rateNum'],
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
    
    #제품/서비스 상태 알아오기   
    def get_status(self, uid):
        status=self.db.child("status").child(uid).get().val()
        return status
    def update_status(self, user_id, changed):
        status_info={
            "status": changed
        }
        self.db.child("status").child(user_id).set(status_info)
        return changed
    
    #제품 평점 업데이트 #이제 리뷰가 등록되면 평점 가져오는 코드 추가해야 함
    def update_rate(self, name):
        total=0
        sum=0
        item=self.db.child("item").child(name).child("review").get()
        if(item.val()==None): return 0
        for res in item.each():
            total+=1
            print(res, res.key(), res.val())
            sum+=int(res.val()['rate'])
        rate=round(sum/total,1)
        self.db.child("item").child(name).child("rate").set(rate)
        self.db.child("item").child(name).child("rateNum").set(total)
        return total