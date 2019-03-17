import json
from bs4 import BeautifulSoup
from mongoengine import connect, Document,ListField,StringField


result_lo = {}
result_acad = {}
result = []

class Course_Info(Document):
    course_code = StringField(required = True, primary_key=True)
    course_name = StringField()
    description = StringField()
    outcomes = ListField(StringField())
    def __init__(self, course_code, course_name, description,outcomes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_code = course_code
        self.course_name = course_name
        self.description = description
        self.outcomes = outcomes

def json_to_dict():
    with open("learning_outcomes.json","r",encoding="utf-8") as f:
        content = f.readlines()
        content[0] = content[0][1:]
        content.pop()
        for e in content:
            e = json.loads(e[1:])
            if e["acad_object"] in result_lo:
                result_lo[e["acad_object"]].append(e["description"])
            else:
                result_lo[e["acad_object"]] = [e["description"]]

    with open("acad_objects.json", "r",encoding="utf-8") as f:
        content = f.readlines()
        content[0] = content[0][1:]
        content.pop()
        for e in content:
            e = json.loads(e[1:])
            # print(e)
            if e["type"] != "course":
                continue
            # print(e)
            if e["handbook_description"]:
                des = BeautifulSoup(e["handbook_description"], "html.parser").get_text()
            else:
                des = ""
            result_acad[e["id"]] = {"name":e["name"],"course_code":e["code"],"handbook_description":des}


def upload():
    # connect mongodb and store course info one by one
    connect(host='mongodb://admin:admin@ds139067.mlab.com:39067/my-database')
    # connect('capstone_project')

    for e in result_lo.keys():
        if e not in result_acad.keys():
            continue
        temp = result_acad[e]
        course_info = Course_Info(temp["course_code"],temp["name"],temp["handbook_description"],result_lo[e])
        # result.append({"course_name":temp["name"],"course_code":temp["course_code"],"description":temp["handbook_description"],"learning_outcome":result_lo[e]})
        course_info.save()

