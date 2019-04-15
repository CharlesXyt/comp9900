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
verb_list, key_phrases_list,outcome_list, learning_outcomes = [], [], [], []
course_info=""


# verb options for front-end
verb_wheel = dict({"Remember": ["Recognise", "Identify", "Recall", "Retrieve", "Select"],
                   "Understand": ["Explain", "Describe", "Compare", "Understand",  "Illustrate"],
                   "Apply": ["Interpret", "Apply", "Use", "Practice", "Compute"],
                   "Analyse": ["Integrate", "Analyse", "Organise", "Relate", "Deconstruct"],
                   "Evaluate": ["Evaluate", "Critique", "Review", "Judge", "Justify"],
                   "Create": ["Generate", "Create", "Design", "Construct", "Compose"]})

assess_dict = dict({"Create": ["Blueprint", "Formula", "Invention"],
                    "Evaluate": ["Report", "Survey", "Debate"],
                    "Analyse": ["Diagram", "Investigation", "Outline"],
                    "Apply": ["Demonstration", "Experiment", "Presentation", "Report"],
                    "Understand": ["Debate", "Explanation", "Quiz", "Open-book Exam"],
                    "Remember": ["Quiz", "Recitation", "Close-book Exam"]})
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
            return jsonify("success"), 201
        except Exception:
            return jsonify("error"), 404


@app.route("/generate3", methods=["POST", "GET"])
def generate3():
    global outcome_list
    assess_rec = dict()
    if request.method == "GET":
        try:
            # establish assessments dictionary
            for e in outcome_list:
                e = e.split()
                for key in verb_wheel:
                    if key in assess_rec:
                        continue
                    if e[0].capitalize() in verb_wheel[key]:
                        assess_rec[key] = assess_dict[key]
                        break
            return render_template("generate3.html", outcome_list=outcome_list, course_info=course_info, assess_rec=assess_rec)
        except Exception:
            return jsonify("error"), 404
    if request.method == "POST":
        try:
            outcome_list = []
            response = request.get_json()
            outcome_list = json.loads(response["outcome_list"])
            return jsonify("success"), 201
        except Exception:
            return jsonify("error"), 404


@app.route("/evaluate",methods=["GET","POST"])
def evaluate():
    global learning_outcomes
    if request.method == "GET":
        with open("course_info.json", "r") as f:
            course_list = json.loads(f.read())
            result = {}
            for e in course_list:
                result[e] = None
        return render_template("search-evaluate.html", course_list=result)

    if request.method == "POST":
        try:
            outcome_verbs, result = [], []
            count_len, count_cate, count_nverb = 0, 0, 0
            course_info_all = request.form.get("course_info")
            course_info = course_info_all.split()
            course_code = course_info[0].upper()
            connect("course_info")
            with open("verb_wheel.json","r") as f:
                dict = json.loads(f.read())
            learning_outcomes = json.loads(Course_Info.objects(course_code=course_code).to_json())[0]["outcomes"]


            # check how many words are not verbs
            verb_wheel_list = [e for key in dict for e in dict[key]]

            # remove messy characters and check the length of this learning outcome
            for i in range(len(learning_outcomes)):
                learning_outcomes[i] = re.sub(r"â\?\?",'',learning_outcomes[i])
                e = learning_outcomes[i].split()
                e[0]= e[0].capitalize()
                learning_outcomes[i] = " ".join(e)
                if len(e) <= 3:
                    count_len+=1
                    result.append(0)
                    continue
                if e[0].lower() == "to":
                    outcome_verbs.append(e[1])
                else:
                    outcome_verbs.append(e[0])
                outcome_verbs[-1] = re.sub(r"[^A-Za-z]","",outcome_verbs[-1])
                if outcome_verbs[-1].capitalize() not in verb_wheel_list:
                    result.append(0)
                    continue
                result.append(1)

            # check how many covered of 6 categories
            for e in dict.keys():
                for word in outcome_verbs:
                    if word in dict[e]:
                        count_cate+=1
                        break

            return render_template("evaluate.html", course_info=course_info_all,learning_outcomes=learning_outcomes,result=result,count_cate=count_cate)
        except Exception:
            return jsonify("error"), 404


if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    connect("course_info")
    app.run(port=8000, debug=True)
