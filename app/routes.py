from flask import Flask,request,jsonify,url_for
from flask import render_template
from upload_dataset import Course_Info
from mongoengine import connect
import json
import re
from boto3.session import Session

app = Flask(__name__)
aws_key = ""
aws_secret = ""


@app.route("/")
def home():
   return render_template("index.html")

@app.route("/generate", methods = ['GET',"POST"])
def generate():
    if request.method == "GET":
        with open("course_info.json","r") as f:
            course_list = json.loads(f.read())
            result = {}
            for e in course_list:
                result[e] = None
        with open("credential","r") as f:
            global aws_key,aws_secret
            aws_key = f.readline().split(":")[1]
            aws_secret = f.readline().split(":")[1]
            aws_key = aws_key.rstrip()
            aws_secret = aws_secret.rstrip()
        return render_template("mainpage-new.html",course_list=result)
    if request.method =="POST":
        course_id = request.form.get("course_info").split(" - ")[0]
        connect("course_info")
        try:

            result = Course_Info.objects(course_code=course_id)
            print(json.loads(result.to_json()))
            description = json.loads(result.to_json())[0]["description"]
            description = re.sub(r"[\n]"," ",description)
            print(description)
            session = Session(aws_access_key_id=aws_key,
                              aws_secret_access_key=aws_secret,
                              region_name="ap-southeast-2")
            client = session.client("comprehend")
            cc = client.batch_detect_key_phrases(
                TextList=[
                    description
                ],
                LanguageCode='en'
            )
            print(cc)
            result = set()
            for e in cc["ResultList"][0]["KeyPhrases"]:
                result.add(e["Text"])
            print(result)
            return jsonify(list(result)),200
        except Exception:
                return jsonify("error message"),404


if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    app.run(port=8000, debug=True)

