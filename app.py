from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 이미지가 저장될 폴더 설정
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    title = request.form['title']
    content = request.form['content']
    rating = request.form['rating']
    image_file = request.files['image']

    # 이미지 파일이 첨부되었는지 확인
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)  # 이미지 파일 저장
        image_url = url_for('static', filename='uploads/' + filename)
    else:
        image_url = None

    # 상품리뷰상세 페이지로 데이터 전달
    return render_template('상품리뷰상세.html', title=title, content=content, rating=rating, image_url=image_url)

@app.route('/write_review')
def write_review():
    return render_template('리뷰작성.html')

if __name__ == '__main__':
    app.run(debug=True)
