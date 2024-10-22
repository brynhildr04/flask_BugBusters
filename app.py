from flask import Flask, render_template, request
import sys
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("index.html")
@application.route("/home.html")
def view_home():
    return render_template("home.html")
@application.route("/cart.html")
def view_cart():
    return render_template("cart.html")
@application.route("/profile.html")
def view_profile():
    return render_template("profile.html")
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():

    image_url = "https://search.pstatic.net/common/?src=https%3A%2F%2Fshop-phinf.pstatic.net%2F20240925_172%2F1727257588232P8xXD_JPEG%2F42154487053458405_564187763.jpg&type=sc960_832"

    data = request.form
    return render_template("result.html", data=data, img_path=image_url)
                
if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True)


