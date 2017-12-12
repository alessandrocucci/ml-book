import json
import sqlite3
import requests
import pickle
import string

from nltk.corpus import stopwords
from nltk.stem.snowball import ItalianStemmer
from nltk import word_tokenize

import tensorflow as tf
import numpy as np

from tflearn import input_data, fully_connected, regression, DNN

from flask import Flask, request

TOKEN = ""

app = Flask(__name__)

d = pickle.load(open("corpus.p", "rb"))
temi = d['temi']
classi = d['classi']
documenti = d['documenti']

database = "bot.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()

stemmer = ItalianStemmer()
stop = set(stopwords.words('italian'))


def genera_temi(testo):
    stop = set(stopwords.words('italian'))
    lista_parole = word_tokenize(testo)
    temi = [
        stemmer.stem(p.lower()) for p in lista_parole
        if p not in stop and p not in string.punctuation
    ]
    return temi


def genera_input(lista_temi):
    lista_input = [0] * len(temi)
    for tema in lista_temi:
        for i, t in enumerate(temi):
            if t == tema:
                lista_input[i] = 1
    return (np.array(lista_input))


def BotANN():
    tf.reset_default_graph()

    rete = input_data(shape=[None, len(temi)])
    rete = fully_connected(rete, 8)
    rete = fully_connected(rete, 8)
    rete = fully_connected(rete, len(classi), activation='softmax')
    rete = regression(rete)

    model = DNN(rete, tensorboard_dir='logs')
    return model


modello = BotANN()
modello.load("./rete")


SOGLIA_ERRORE = 0.25


def classifica(modello, array):
    # genera le probabilità
    prob = modello.predict([array])[0]
    # filtro quelle che superano la soglia
    risultati = [
        [i,p] for i,p in enumerate(prob)
        if p > SOGLIA_ERRORE
    ]
    # ordino per le classi più probabili
    risultati.sort(key=lambda x: x[1], reverse=True)
    lista_classi = []
    for r in risultati:
        lista_classi.append((list(classi)[r[0]], r[1]))
    return lista_classi


@app.route('/', methods=['GET', 'POST'])
def risponditore():
    if request.method == 'GET':
        # Quando registriamo un endpoint a un webhook, dobbiamo
        # restituire la 'hub.challenge', un parametro che
        # serve a Facebook.
        if request.args.get("hub.mode") == "subscribe" and \
                request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == TOKEN:
                return "Token errato", 403
            return request.args["hub.challenge"], 200

        return "Sono un bot, non un sito web", 200
    elif request.method == 'POST':
        # è appena arrivato un messaggio
        data = request.get_json()
        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    utente = messaging_event["sender"]["id"]
                    domanda = messaging_event["message"]["text"]
                    risposta = elabora_risposta(domanda, utente)
                    invia(utente, risposta)
        return "ho risposto", 200


def invia(utente, messaggio):
    params = {
        "access_token": TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": utente
        },
        "message": {
            "text": messaggio
        }
    })
    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


contesti = {}


def elabora_risposta(frase, utente="utente_prova"):
    temi_frase = genera_temi(frase)
    X = genera_input(temi_frase)
    classi_predette = classifica(modello, X)
    # tolgo le probabilità
    classi_predette = [c[0] for c in classi_predette]

    if classi_predette:
        # ho un contesto settato?
        if contesti.get(utente):
            contesto = contesti[utente]

            # quali classi hanno questo contesto?
            q = """
                SELECT classe FROM classi
                INNER JOIN contesti ON (classi.id = contesti.id_classe)
                WHERE classe IN ({})
            """.format(",".join(
                "'{}'".format(classe) for classe in classi_predette
            )
            )
            filtro_classi = [c[0] for c in cursor.execute(q).fetchall()]
            if filtro_classi:
                # ho almeno una classe predetta che usa un contesto
                classi_predette = [c for c in classi_predette]

        # leggo le risposte
        q = """
            SELECT risposta 
            FROM risposte
            INNER JOIN classi ON (risposte.id_classe = classi.id)
            WHERE classe = '{0}'
        """.format(classi_predette[0])
        risposte = [r[0] for r in cursor.execute(q).fetchall()]

        # scelgo una risposta
        risposta = np.random.choice(risposte)

        # imposto il contesto, se c'è
        q = """
            SELECT contesto from contesti
            INNER JOIN classi ON (contesti.id_classe = classi.id)
            INNER JOIN risposte ON (risposte.id_classe = classi.id)
            WHERE risposta = "{}"
        """.format(risposta)
        contesto = cursor.execute(q).fetchone()
        contesti[utente] = contesto[0] if contesto else None

        return risposta


if __name__ == '__main__':
    app.run(debug=True)