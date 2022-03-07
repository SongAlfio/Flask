from flask import Flask, render_template
import random
from datetime import datetime
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("Esercizio1.html")

@app.route('/meteo', methods=['GET'])
def Meteo():
    n = random.randint(0, 8)
    if n <= 2:
      previsione = 'pioggia'
      tempo = 'pioggia'
    else:
      if n >= 3 & n < 5:
        previsione = 'nuvoloso'
        tempo = 'nuvoloso'
      if n > 5:
        previsione = 'sole'
        tempo = 'sole'
    return render_template("Esercizio1_meteo.html", pr = previsione, tp = tempo)


@app.route('/frasicelebri', methods=['GET'])
def Frase():
  Frasi_Autori = {
    0 : 'Innamorati di te, della vita e dopo di chi vuoi.(Frida Kahlo)',
    1 : 'Contro la stupidità non abbiamo difese.(Dietrich Bonhoeffer)',
    2 : 'Il divertimento è una cosa seria.(Italo Calvino)',
    3 : 'Chi non ha bisogno di niente non è mai povero.(Voltaire)',
    4 : 'Non importa quanto vai piano, l importante è non fermarsi.(Confucio)',
    5 : 'Prendete in mano la vostra vita e fatene un capolavoro.(Papa Giovanni Paolo II)',
    6 : 'Maggiore è l ostacolo, maggiore è la gloria nel superarlo.(Molière)',
    7 : 'Più dura è la battaglia, più dolce è la vittoria.(Les Brown)',
    8 : 'Il segreto per andare avanti è iniziare.(Mark Twain)',
    9 : 'L ironia è sprecata quando si usa sugli stupidi.(Oscar Wilde)'
  }
  n1 = random.randint(0, 9)
  frase = Frasi_Autori[n1]
  
  if n1 == 0:
    image = 'Frida_Kahlo'
  else:
    if n1 == 1:
      image = 'Dietrich_Bonhoeffer'
    if n1 == 2:
      image = 'Italo_Calvino'
    if n1 == 3:
      image = 'Voltaire'
    if n1 == 4:
      image = 'Confucio'
    if n1 == 5:
      image = 'Papa_Giovanni_Paolo_II'
    if n1 == 6:
      image = 'Molière'
    if n1 == 7:
      image = 'Les Brown'
    if n1 == 8:
      image = 'Mark_Twain'
    if n1 == 9:
      image = 'Oscar_Wilde'
  return render_template("Esercizio1_frase.html",frase = frase,immagini = image)

@app.route('/quantomanca', methods=['GET'])
def Calendario():
  oggi = datetime.now()
  vacanza = datetime(day=8, month=6, year=2022)
  differenza = vacanza - oggi
  return render_template("Esercizio1_calendario.html", vacanza = differenza.days)    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)