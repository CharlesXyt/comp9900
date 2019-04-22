from flask import Flask,jsonify,request
from upload_dataset import Course_Info
from mongoengine import connect
import json


app = Flask(__name__)

@app.route("/", methods = ['GET'])
def get_course_list():
    course_list = []
    connect('course_info')
    for e in Course_Info.objects:
        course_info = e.to_json()
        course_info = json.loads(course_info)
        course_code = course_info["_id"]
        course_name = course_info["course_name"]
        course_list.append( course_code + " - " + course_name )
    return jsonify(course_list), 200

if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    app.run(debug=True)
