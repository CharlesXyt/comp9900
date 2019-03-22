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
    with open("course_info.json","r") as f:
        course_list = json.loads(f.read())
    return render_template("mainpage.html",course_list=course_list)

if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    app.run(port=8000, debug=True)

