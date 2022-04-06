#realizzare un server web che permetta di effetuare il login
#l'utente inserisce lo user name e la password
#se lo user name è admin e la password è 123xxx## 
#il sito ci saluta con un messaggio di benvenuto
#altrimenti ci dà iln messaggio di errore
from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("app_Esercizio1/Form1.html")

@app.route('/data', methods=['GET'])
def Dati_Utenti():
    nome = request.args['Name']
    password = request.args['Password']
    if nome == 'admin':
        if password == '123xxx##':
            return render_template("app_Esercizio1/Welcome.html",nome = nome)
        else:
            return ('Password sbagliato')
    else:
        return('Utente sbagliato')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)