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
    def get_user(self, id_):
        users=self.db.child("user").get()
        for res in users.each():
            value=res.val()
            if(value['id']==id_):
                return res.val()
        return None
    
    def get_items(self):
        items=self.db.child("item").get().val()
        return items 
    
    #제품/서비스 각각 전체 체품 가져오기
    def get_items_byproductType(self, product_type):
        items=self.db.child("item").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value=res.val()
            key_value=res.key()
            if(value['product_type']==product_type):
                target_value.append(value)
                target_key.append(key_value)

        print("######target_value", target_value)
        new_dict={}
        for k, v in zip(target_key, target_value):
            new_dict[k]=v
        return new_dict
    
    #카테고리별 제품 가져오기
    def get_items_byCategory(self, cate):
        data=self.db.child("item").get()
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
    
    #좋아요 목록 가져오기
    def get_heart_byId(self, uid):
        hearts=self.db.child("heart").child(uid).get().val()
        return hearts
    
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
    
    #카트
    def get_cart(self, uid):
        items=self.db.child("cart").child(uid).get().val()
        return items
    def add_to_cart(self, uid, data):
        quantity=int(data['quantity'])
        price=int(self.db.child("item").child(data['name']).child("price").get().val())
        total=quantity*price
        cart_info={
            "quantity": quantity,
            "price": price,
            "total": total,
            "img_path": self.db.child("item").child(data['name']).child("img_path").get().val()
        }
        self.db.child("cart").child(uid).child(data['name']).set(cart_info)
        return 1
    def calc_total(self, uid):
        items=self.db.child("cart").child(uid).get()
        total=0
        if(items.val()==None): return total
        for res in items.each():
            total+=res.val()['total']
        return total
    def remove_item(self, uid, name):
        self.db.child("cart").child(uid).child(name).remove()
        return 1
    def update_quantity(self, uid, name, changed):
        price=int(self.db.child("item").child(name).child("price").get().val())
        total=price*int(changed)
        self.db.child("cart").child(uid).child(name).update({"quantity": changed})
        self.db.child("cart").child(uid).child(name).update({"total": total})
        return self.db.child("cart").child(uid).child(name).get().val()
    def clear_cart(self, uid):
        self.db.child("cart").child(uid).remove()
        return 0
    
    
    # 게시글 저장
    def save_post(self, data, user_id, date):
        
        post_info = {
            "id": user_id,
            "item_name": data['item_name'],
            "name": data["writer"],         # 작성자 이름 #가져오기 너무 빡센데
            "title": data["postTitle"],   # 게시물 제목
            "content": data["postContent"],  # 게시물 내용
            "date": date,                 # 작성 날짜
            "views": 0                    # 초기 조회수
        }
        try:
            # Firebase 경로 수정: post/{user_id}/{post_id}
            self.db.child("post").child(data['item_name']).push(post_info)
            return data['item_name']
        except Exception as e:
            print(f"Error saving post: {e}")
            return None
    
    # 특정 제품 하위의 게시글 가져오기
    def get_post_by_name(self, item_name):
        post_ref = self.db.child("post").child(item_name).get().val()
        return post_ref

    # 특정 게시글 가져오기
    def get_post_by_key(self, item_name, key):
        post=self.db.child("post").child(item_name).child(key).get().val()
        return post

    # 특정 게시글 조회수 증가
    def increment_views(self, user_id, key):
        post = self.db.child("post").child(user_id).child(key).get().val()  # 올바른 경로
        updated_views=int(post['views'])+1
        self.db.child("post").child(user_id).child(key).update({"views": updated_views})  # 조회수 업데이트
        return updated_views





        




    
    




