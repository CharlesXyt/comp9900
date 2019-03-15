from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def home():
   return render_template("landingpage.html")

@app.route("/generate")
def generate():
   return render_template("mainpage.html")
   
if __name__ == '__main__':
   app.run(debug=True)

