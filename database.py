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