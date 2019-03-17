import requests,json
import pandas as pd

# all address for useful data
url_list=["https://cdn.teaching.unsw.edu.au/aims2-uat/acad_graduate_capabilities.json",
"https://cdn.teaching.unsw.edu.au/aims2-uat/acad_objects.json" ,
"https://cdn.teaching.unsw.edu.au/aims2-uat/as_map_lo.json" ,
"https://cdn.teaching.unsw.edu.au/aims2-uat/assessments.json" ,
"https://cdn.teaching.unsw.edu.au/aims2-uat/learning_outcomes.json",
"https://cdn.teaching.unsw.edu.au/aims2-uat/lo_map_gc.json" ]

#download and save them
all_content = [requests.get(e).content for e in url_list]
filename =[e.split("/")[-1] for e in url_list]
for i in range(len(filename)):
    with open(filename[i],"wb") as f:
        f.write(all_content[i])

#create a dictionary stores all data
result_dic = {}
for e in ["acad_objects.json","learning_outcomes.json","assessments.json","learning_outcomes.json"]:
    with open(e,"r",encoding="utf-8") as f:
        content = f.readlines()
        content[0] = content[0][1:]
        content.pop()
        content = {json.loads(e[1:])["id"]:json.loads(e[1:]) for e in content}
        result_dic[e.split(".")[0]] = content

for e in ["as_map_lo.json","lo_map_gc.json"]:
    with open("as_map_lo.json","r",encoding="utf-8") as f:
        content = f.readlines()
        content[0] = content[0][1:]
        content.pop()
        content = {e:json.loads(e[1:]) for e in content}
        result_dic[e.split(".")[0]] = content

#collect the useful columns and save as file for use
acad_result = []
for e in result_dic["learning_outcomes"].keys():
    rl = result_dic["learning_outcomes"][e]
    ra = result_dic["acad_objects"]
    acad_num = rl["acad_object"]
    acad_result.append({"id":e,"career":ra[acad_num]["career"],"name":ra[acad_num]["name"],"handbook_description":ra[acad_num]["handbook_description"],"additional_info":ra[acad_num]["additional_info"], "type":ra[acad_num]["type"],"learning_outcome":rl["description"]})
new = pd.DataFrame(acad_result)
columns = ["id","career","name","handbook_description","additional_info","type","learning_outcome"]
new.to_csv("all_information.csv",sep=',',index=False,columns=columns,encoding="utf-8")

map_result = []
for e in result_dic["as_map_lo"].keys():
    rass_id = result_dic["as_map_lo"][e]["assessment"]
    rlo_id = result_dic["as_map_lo"][e]["learning_ou tcome"]
    ra = result_dic["assessments"]
    rl = result_dic["learning_outcomes"]
    map_result.append({"course_code":ra[rass_id]["course"],"assessment":ra[rass_id]["title"],"description":ra[rass_id]["description"],"weight":ra[rass_id]["weight"],"learning_outcome":rl[rlo_id]["description"]})
new = pd.DataFrame(map_result)
columns = ["course_code","assessment","description","weight","learning_outcome"]
new.to_csv("as_map_lo.csv",sep=',',index=False,columns=columns,encoding="utf-8")