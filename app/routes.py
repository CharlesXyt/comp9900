from flask import Flask
from flask import render_template
from upload_dataset import Course_Info
from mongoengine import connect
import json

app = Flask(__name__)

@app.route("/")
def home():
   return render_template("landingpage.html")

@app.route("/generate", methods = ['GET'])
def generate():
    course_list = []
    connect('course_info')
    for e in Course_Info.objects:
        course_info = e.to_json()
        course_info = json.loads(course_info)
        course_code = course_info["_id"]
        course_name = course_info["course_name"]
        course_list.append(course_code + " - " + course_name)
    return render_template("mainpage.html", course_list = course_list)

if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    app.run(port=8000, debug=True)

