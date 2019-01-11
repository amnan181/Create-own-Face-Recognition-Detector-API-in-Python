from flask import Flask,jsonify,request
from flask_cors import CORS
import os
import face_recognition
app = Flask(__name__)
images = os.listdir('images')
CORS(app)

@app.route('/')
def index():
    return 'Server Succesfuly Running!'

@app.route('/upload',methods=['GET','POST'])
def upload():
    image = request.files['file']
    image_to_be_matched = face_recognition.load_image_file(image)
    try:
        image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
    except IndexError:
        return jsonify({'success':'false','message':'No face found in the image'})
    for image in images:
        current_image = face_recognition.load_image_file("images/" + image)
        current_image_encoded = face_recognition.face_encodings(current_image)[0]
        result = face_recognition.compare_faces(
            [image_to_be_matched_encoded], current_image_encoded)
        if result[0] == True:
            return jsonify({'success':'true',"Matched" : image.rsplit('.')[0]})
    return jsonify({'success':'false'})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=2020,debug=True)
