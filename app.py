from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/product-detail")
def productdetail():
    return render_template("제품 상세 페이지.html")

@application.route("/product-detail")
def servicedetail():
    return render_template("리뷰 상세 페이지.html")

                
if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)
