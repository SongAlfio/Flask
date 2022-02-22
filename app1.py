from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])#è il home page
def hello_world():
    return render_template("index.html", testo="Hello,World!")

@app.route('/it', methods=['GET'])
def ciao_mondo():
    return render_template("index.html", testo="Ciao,Mondo!")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)