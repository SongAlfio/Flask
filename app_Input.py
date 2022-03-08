from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("Form.html")

@app.route('/data', methods=['GET'])
def Dati_Utenti():
    nome = request.args['Name']
    return render_template("Welcome.html",nome = nome)
   #return nome      ci fa vedere solo il Name

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)