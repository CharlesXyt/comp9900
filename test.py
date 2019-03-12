from flask import Flask,render_template,request,redirect,session

app = Flask(__name__) 
app.secret_key = 'u2jksidjflsduwerjl'
app.debug = True
USER_DICT = {
    0: {'course_code':'COMP9021','course_name':'Principles of Programming'},
    1: {'course_code':'COMP9900','course_name':'Information Technology Project'},
    2: {'course_code':'COMP9336','course_name':'Mobile Data Networking'},
    3:{'course_code':'COMP9334','course_name':'Capacity Planning of Computer Systems and Networks'},
    4:{'course_code':'COMP9024','course_name':'Data Structures and Algorithms'},
    5:{'course_code':'COMP9444','course_name':'Neural Networks and Deep Learning'},
}


#main page
@app.route('/', methods=['GET'])
def hello():
    return render_template('main.html')

#placeholder for now
@app.route('/placeholder')
def temp():
    cid = request.args.get('search')                #cid is something like COMP9021 now
    i = 0
    while i< len(USER_DICT):
        if cid == USER_DICT[i]['course_code'] or cid == USER_DICT[i]['course_name']:
            return render_template('placeholder.html',info = ('This is a placeholder for ' + USER_DICT[i]['course_code'] + '.'))
        i = i+1
    return render_template('placeholder.html',info = 'Can\'t find your input info. Click the button at the bottom right corner to return.')


# login system
@app.route('/login',methods=['GET',"POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user') # get what POST passed
    pwd = request.form.get('pwd') # get what POST passed
    if user == 'admin' and pwd == '123456':
        # all user info in one session
        session['user_info'] = user
        return redirect('/index')
    else:
        return render_template('login.html',msg ='Wrong username or password')

#page after logged in
@app.route('/index',endpoint='n1')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')

    return render_template('index.html',user_dict = USER_DICT)

#detail
@app.route('/detail')
def detail():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')

    uid = int(request.args.get('uid'))             #uid is something like 3 now
    info = USER_DICT[uid]

    return render_template('detail.html',info = info)


#logout-delete session
@app.route('/logout')
def logout():
    del session['user_info']
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000')
