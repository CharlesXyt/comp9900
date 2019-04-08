from flask import Flask,request,jsonify,url_for
from flask import render_template
from upload_dataset import Course_Info
from mongoengine import connect
import json,re,nltk
from nltk.corpus import stopwords
from boto3.session import Session

app = Flask(__name__)
aws_key = ""
aws_secret = ""
verb_list, key_phrases_list = [], []
verb_wheel = dict({"Remember": ["Recognise", "Identify", "Recall", "Retrieve", "Select"],
                   "Understand": ["Explain", "Describe", "Compare", "Understand",  "Illustrate"],
                   "Apply": ["Interpret", "Apply", "Use", "Practice", "Compute"],
                   "Analyse": ["Integrate", "Analyse", "Organise", "Relate", "Deconstruct"],
                   "Evaluate": ["Evaluate", "Critique", "Review", "Judge", "Justify"],
                   "Create": ["Generate", "Create", "Design", "Construct", "Compose"]})
nltk.download('stopwords')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=['GET', "POST"])
def generate():
    if request.method == "GET":
        with open("course_info.json", "r") as f:
            course_list = json.loads(f.read())
            result = {}
            for e in course_list:
                result[e] = None
        with open("credential", "r") as f:
            global aws_key,aws_secret
            aws_key = f.readline().split(":")[1]
            aws_secret = f.readline().split(":")[1]
            aws_key = aws_key.rstrip()
            aws_secret = aws_secret.rstrip()
        return render_template("search-generate.html", course_list=result)

    if request.method == "POST":
        # course_id = request.form.get("course_info").split(" - ")[0].upper()
        # connect("course_info")
        # try:
        #     result = Course_Info.objects(course_code=course_id)
        #     description = json.loads(result.to_json())[0]["description"]
        #     description = re.sub(r"[\n]"," ",description)
        #     session = Session(aws_access_key_id=aws_key,
        #                       aws_secret_access_key=aws_secret,
        #                       region_name="ap-southeast-2")
        #     client = session.client("comprehend")
        #
        #     #response from AWS
        #     cc = client.batch_detect_key_phrases(
        #         TextList=[
        #             description
        #         ],
        #         LanguageCode='en'
        #     )
        #     result = set()
        #     parttern = re.compile("[a-z]{4}\d{4}")
        #     for e in cc["ResultList"][0]["KeyPhrases"]:
        #         e = e["Text"]
        #         temp = e.lower()
        #         if temp.find("student") != -1 or temp.find("course") != -1 or temp.find("unsw")!=-1 or temp.find("study")!=-1 or parttern.findall(temp):
        #             continue
        #         temp = nltk.word_tokenize(temp)
        #         filter_word = [word for word in temp if word not in stopwords.words('english')]
        #         if len(filter_word) <= 1:
        #             continue
        #         result.add(e)
        #     return render_template("new-generate1.html", list=list(result), verb_wheel = verb_wheel)
        # except Exception:
        #         return jsonify("error message"),404
        result = ["labs and programming projects", "data types", "any prior computing knowledge", "the full range", "program structures", "extensive practical work", "overlapping material", "data structures", "Additional Information", "code quality", "all CSE majors", "reflective practice", "a high level programming language", "storage structures"]
        return render_template("generate1.html", list=list(result), verb_wheel=verb_wheel)


@app.route("/generate2", methods=["POST", "GET"])
def generate2():
    global verb_list, key_phrases_list
    if request.method == "GET":
        return render_template("generate2.html", verb_list=verb_list, key_phrases_list=key_phrases_list)

    if request.method == "POST":
        try:
            response = request.get_json()
            print(response)
            verb_list = json.loads(response["Verbs"])
            print(verb_list)
            key_phrases_list = json.loads(response["Key_phrases"])
            print(key_phrases_list)
            key_phrases_list = [e[:-6] for e in key_phrases_list]
            return jsonify("success"), 200
        except Exception:
            return jsonify("error"), 404


@app.route("/generate3", methods=["POST", "GET"])
def generate3():

    return render_template("generate3.html")


if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    app.run(port=8000, debug=True)
