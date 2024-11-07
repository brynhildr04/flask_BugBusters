from flask import Flask, render_template, redirect, url_for

application = Flask(__name__)

# 기본 페이지 설정: purchase_p.html
@application.route('/')
def home():
    return render_template('purchase_product.html')

# 특정 버튼을 클릭하면 payment.html로 이동하는 경로 설정
@application.route('/payment.html')
def view_payment():
    return render_template('payment.html')

# 기타 독립적인 페이지
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


if __name__ == '__main__':
    application.run(debug=True)

