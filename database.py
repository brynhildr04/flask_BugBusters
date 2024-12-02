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
            "price": data['price'],
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
    
    #제품/서비스 각각 전체 체품 가져오기
    def get_items_byproductType(self, category):
        items=self.db.child("item").get()
        target_value=[]
        target_key=[]
        if(category=="product" or category=="service"):
            for res in items.each():
                value=res.val()
                key_value=res.key()
                if(value['product_type']==category):
                    target_value.append(value)
                    target_key.append(key_value)
        else:
            for res in items.each():
                value=res.val()
                key_value=res.key()
                if(value['category']==category):
                    target_value.append(value)
                    target_key.append(key_value)

        print("######target_value", target_value)
        new_dict={}
        for k, v in zip(target_key, target_value):
            new_dict[k]=v
        return new_dict
    
    #카테고리별 제품 가져오기
    def get_items_byCategory(self, data, cate):
        target_value=[]
        target_key=[]
        for res in data.each():
            value=res.val()
            key_value=res.key()
            if(value['category']==cate):
                target_value.append(value)
                target_key.append(key_value)
        new_dict={}
        for k, v in zip(target_key, target_value):
            new_dict[k]=v
        return new_dict
    
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
    
    # 게시글 저장
    def save_post(self, data, user_id, date):
        post_info = {
            "name": data["name"],         # 작성자 이름
            "title": data["postTitle"],   # 게시물 제목
            "content": data["postContent"],  # 게시물 내용
            "user_id": user_id,           # 작성자 ID
            "date": date,                 # 작성 날짜
            "views": 0                    # 초기 조회수
        }
        # Firebase에 게시글 저장 및 고유 키 반환
        key = self.db.child("post").child(data["name"]).push(post_info).get("name")
        print(f"Post saved with key: {key}")  # 디버깅 메시지
        return key

    
    # 고유 키로 특정 게시글 가져오기
    def get_post_by_key(self, name, key):
        try:
            # Firebase에서 고유 키를 기반으로 특정 게시글 가져오기
            post = self.db.child("post").child(name).child(key).get()
            return post.val() if post.val() else None
        except Exception as e:
            print(f"Error fetching post by key: {e}")
            return None
        
    # 모든 게시글 목록 가져오기
    def get_all_posts(self):
        try:
            posts = self.db.child("post").get()
            result = []
            if posts.each():
                for user_posts in posts.each():  # 각 사용자의 게시글
                    for key, post in user_posts.val().items():
                        post["key"] = key  # 게시글 고유 키 추가
                        post["name"] = user_posts.key()  # 작성자 추가
                        result.append(post)
            print(f"Fetched posts: {result}")  # 디버깅 메시지
            return result
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []


    # 특정 게시글 조회수 증가
    def increment_views(self, name, key):
        try:
            post = self.db.child("post").child(name).child(key).get()
            if post.val():
                current_views = post.val().get("views", 0)
                self.db.child("post").child(name).child(key).update({"views": current_views + 1})
        except Exception as e:
            print(f"Error updating views: {e}")
        




    
    




