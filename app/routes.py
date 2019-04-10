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
verb_list, key_phrases_list,outcome_list = [], [], []
course_info=""
verb_wheel = dict({"Remember": ["Recognise", "Identify", "Recall", "Retrieve", "Select"],
                   "Understand": ["Explain", "Describe", "Compare", "Understand",  "Illustrate"],
                   "Apply": ["Interpret", "Apply", "Use", "Practice", "Compute"],
                   "Analyse": ["Integrate", "Analyse", "Organise", "Relate", "Deconstruct"],
                   "Evaluate": ["Evaluate", "Critique", "Review", "Judge", "Justify"],
                   "Create": ["Generate", "Create", "Design", "Construct", "Compose"]})
nltk.download('stopwords')
nltk.download('punkt')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=['GET', "POST"])
def generate():
    global course_info
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
        course_info = request.form.get("course_info").split(" - ")
        course_code = course_info[0].upper()
        connect("course_info")
        try:
            result = Course_Info.objects(course_code=course_code)
            description = json.loads(result.to_json())[0]["description"]
            description = re.sub(r"[\n]"," ",description)
            session = Session(aws_access_key_id=aws_key,
                              aws_secret_access_key=aws_secret,
                              region_name="ap-southeast-2")
            client = session.client("comprehend")

            #response from AWS
            cc = client.batch_detect_key_phrases(
                TextList=[
                    description
                ],
                LanguageCode='en'
            )
            result = set()
            parttern = re.compile("[a-z]{4}\d{4}")
            for e in cc["ResultList"][0]["KeyPhrases"]:
                e = e["Text"]
                temp = e.lower()
                if temp.find("student") != -1 or temp.find("course") != -1 or temp.find("unsw")!=-1 or temp.find("study")!=-1 or parttern.findall(temp):
                    continue
                temp = nltk.word_tokenize(temp)
                filter_word = [word for word in temp if word not in stopwords.words('english')]
                if len(filter_word) <= 1:
                    continue
                result.add(e)
            return render_template("generate1.html", list=list(result), verb_wheel = verb_wheel)
        except Exception:
                return jsonify("error message"),404
        # result = ["labs and programming projects", "data types", "any prior computing knowledge", "the full range", "program structures", "extensive practical work", "overlapping material", "data structures", "Additional Information", "code quality", "all CSE majors", "reflective practice", "a high level programming language", "storage structures"]
        # return render_template("generate1.html", list=list(result), verb_wheel=verb_wheel)


@app.route("/generate2", methods=["POST", "GET"])
def generate2():
    global verb_list, key_phrases_list
    if request.method == "GET":
        return render_template("generate2.html", verb_list=verb_list, key_phrases_list=key_phrases_list)

    if request.method == "POST":
        try:
            response = request.get_json()
            verb_list = json.loads(response["Verbs"])
            key_phrases_list = json.loads(response["Key_phrases"])
            key_phrases_list = [e[:-6] for e in key_phrases_list]
            return jsonify("success"), 200
        except Exception:
            return jsonify("error"), 404


@app.route("/generate3", methods=["POST", "GET"])
def generate3():
    global outcome_list
    if request.method == "GET":
        return render_template("generate3.html",outcome_list=outcome_list,course_info=course_info)
    if request.method == "POST":
        try:
            outcome_list = []
            response = request.get_json()
            outcome_list = json.loads(response["outcome_list"])
            return jsonify("success"), 200
        except Exception:
            return jsonify("error"), 404


@app.route("/evaluate",methods=["GET","POST"])
def evaluate():
    if request.method == "GET":
        with open("course_info.json", "r") as f:
            course_list = json.loads(f.read())
            result = {}
            for e in course_list:
                result[e] = None
        return render_template("search-evaluate.html", course_list=result)
    if request.method == "POST":
        course_info = request.form.get("course_info").split(" - ")
        course_code = course_info[0].upper()
        connect("course_info")
        with open("verb_wheel.json","r") as f:
            dict = json.loads(f.read())
        learning_outcomes = json.loads(Course_Info.objects(course_code=course_code).to_json())[0]["outcomes"]

        outcome_verbs = []
        count = 0
        for e in learning_outcomes:
            e = re.sub(r"â\?\?",'',e)
            e = e.split()
            if(e[0].lower() == "to"):
                outcome_verbs.append(e[1])
            else:
                outcome_verbs.append(e[0])
        for word in outcome_verbs:
            for e in dict.keys():
                if word in dict[e]:
                    count+=1
        print(count)


if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    connect("course_info")
    with open("verb_wheel.json", "r") as f:
        dict = json.loads(f.read())
    learning_outcomes = json.loads(Course_Info.objects(course_code="GENM0202").to_json())[0]["outcomes"]
    outcome_verbs = []
    count = 0
    for e in learning_outcomes:
        e = re.sub(r"â\?\?", '', e)
        e = e.split()
        if (e[0].lower() == "to"):
            outcome_verbs.append(e[1])
        else:
            outcome_verbs.append(e[0])
    for e in dict.keys():
        for word in outcome_verbs:
            word = word.capitalize()
            if word in dict[e]:
                count += 1
                break
    print(count)
    # app.run(port=8000, debug=True)
