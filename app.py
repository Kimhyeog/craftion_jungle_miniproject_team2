
# 필요한 라이브러리 import
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def mainPage() :
  return render_template("index.html")

if __name__ == "__main__" :
  app.run("0.0.0.0",port=3000,debug=True)



