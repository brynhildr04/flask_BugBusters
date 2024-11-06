from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__)  # Flask 인스턴스 생성
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route("/")
def home():
    return render_template("상품등록하기.html")

@app.route("/상품등록하기")
def view_register():
    return render_template("상품등록하기.html")

@app.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    data = {
        "title": request.form.get("title", ""),
        "product_type": request.form.get("product_type", ""),
        "category": request.form.get("category", ""),
        "description": request.form.get("description", "")
    }
    img_path = None
    
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            img_path = url_for('static', filename='images/' + image.filename)

    return render_template("상품등록결과.html", data=data, img_path=img_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
