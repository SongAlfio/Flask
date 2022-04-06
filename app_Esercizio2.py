#realizzare un sito web che permetta la registrazione dei utenti
#l'utente inserisce il nome, un username, una password
#la conferma della password e il sesso
#se le informazione sono corrette il sito salva le informazioni in una struttura dati opportuna(una lista di dizionario)
#prevedere la possibilità di fare il login inserendo username e password.
#se sono corrette formare un messaggio diverso dal sesso
from flask import Flask, render_template,request
app = Flask(__name__)
lista = []

@app.route('/', methods=['GET'])
def home():
    return render_template("app_Esercizio2/Form2.html")


@app.route('/data', methods=['GET'])
def Dati_Utenti():
    nome_utente = request.args['Username']
    password = request.args['Password']
    nome = request.args['Name']
    password1 = request.args['Password1']
    sesso = request.args['Sex']
    
    if password1 != password:
        return render_template('app_Esercizio2/Errore_Es2.html', messaggio = 'Riconfermare il password')
    else:
        lista.append({'name':nome, 'username':nome_utente, 'password':password, 'sex':sesso})
        print(lista)
        return render_template("app_Esercizio2/Login_Es2.html")

@app.route('/login', methods=['GET'])
def login():
    username_log = request.args['username']
    password_log = request.args['password']
    
    for utente in lista:
        if utente['username'] == username_log and utente['password'] == password_log:
            sesso = utente['sex']
            if sesso == 'M':
                return render_template('Welcome.html', nome = utente['name'], ciao = 'Benvenuto')
            if sesso == 'F':
                return render_template('Welcome.html', nome = utente['name'], ciao = 'Benvenuta')
            if sesso == 'A':
                return render_template('Welcome.html', nome = utente['name'], ciao = 'Ciao')
    return render_template('app_Esercizio2/Errore_Es2.html', messaggio = 'username o password errata')



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)