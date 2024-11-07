from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# 기본 페이지 설정: purchase_p.html
@app.route('/')
def home():
    return render_template('purchase_product.html')

# 특정 버튼을 클릭하면 payment.html로 이동하는 경로 설정
@app.route('/payment')
def view_payment():
    return render_template('payment.html')

# 기타 독립적인 페이지
@app.route('/aboutus')
def view_aboutus():
    return render_template('aboutus.html')

@app.route('/chat_product')
def view_chat_product():
    return render_template('chat_product.html')

@app.route('/chat_service')
def view_chat_service():
    return render_template('chat_service.html')

@app.route('/purchase_service')
def view_purchase_service():
    return render_template('purchase_service.html')


if __name__ == '__main__':
    app.run(debug=True)

