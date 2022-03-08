#realizzare un sito web che permetta la registrazione dei utenti
#l'utente inserisce il nome, un username, una password
#la conferma della password e il sesso
#se le informazione sono corrette il sito salva le informazioni in una struttura dati opportuna(una lista di dizionario)
#prevedere la possibilità di fare il login inserendo username e password.
# #se sono corrette formare un messaggio diverso dal sesso
from flask import Flask, render_template,request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("Form2.html")


@app.route('/data', methods=['GET'])
def Dati_Utenti():
    nome_utente = request.args['Username']
    password = request.args['Password']
    nome = request.args['Name']
    password1 = request.args['Password1']
    sesso = request.args['Sex']
    Informazione_Utenti = dict()
    if password1 != password:
        return ('Riconfermare il password!')
    else:
        return Informazione_Utenti['nome_utente'] == nome_utente
        return Informazione_Utenti['password'] == password
        return Informazione_Utenti['nome'] == nome
        return Informazione_Utenti['sesso'] == sesso
                         
        return render_template("Login.html",Informazione_Utenti = Informazione_Utenti)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)