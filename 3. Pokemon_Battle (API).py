from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import json
import pandas as pd
import requests
import joblib
import random
import os
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='')

@app.route('/')
def welcome():
    return render_template('welcomeujian.html')


@app.route('/hasil', methods=['POST'])
def hasil():
    try:
        nama = request.form['nama'].capitalize()
        nama2 = request.form['nama2'].capitalize()
        print('"Yang diinput dr Web: " Nama :', nama)
        print('"Yang diinput dr Web: " Nama2 :', nama2)
        # df = pd.read_csv('datasetpokemon2.csv')
        db = joblib.load('dfpok1pokemon2')
        model = joblib.load('modelpokemon2')
        try:
            if nama == "":
                return render_template('pokemonerror.html')

            else:
                url = 'https://pokeapi.co/api/v2/pokemon/' + nama.lower()
                url2 = 'https://pokeapi.co/api/v2/pokemon/' + nama2.lower()
                pokemon1 = requests.get(url)
                pokemon2 = requests.get(url2)
                id = pokemon1.json()["id"]
                id2 = pokemon2.json()["id"]
                foto1 = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/"+str(id)+".png"
                foto2 = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/"+str(id2)+".png"

                print(nama)
                print(nama2)
                print('========')

                #Prediksi ===================

                # idpoke1, idpoke2, hp1, hp2, att1, att2, def1, def2, spatt1, spatt2, spdef1, spdef2, speed1, speed2, winner
                id1 = db['#'][db['Name'] == nama].values[0]
                hp1 = db['HP'][db['Name']==nama].values[0]
                att1 = db['Attack'][db['Name']==nama].values[0]
                def1 = db['Defense'][db['Name']==nama].values[0]
                spatt1 = db['Sp. Atk'][db['Name']==nama].values[0]
                spdef1 = db['Sp. Def'][db['Name']==nama].values[0]
                speed1 = db['Speed'][db['Name']==nama].values[0]

                id2 = db['#'][db['Name'] == nama2].values[0]
                hp2 = db['HP'][db['Name']==nama2].values[0]
                att2 = db['Attack'][db['Name']==nama2].values[0]
                def2 = db['Defense'][db['Name']==nama2].values[0]
                spatt2 = db['Sp. Atk'][db['Name']==nama2].values[0]
                spdef2 = db['Sp. Def'][db['Name']==nama2].values[0]
                speed2 = db['Speed'][db['Name']==nama2].values[0]

                # print(id1, id2, hp1, hp2, att1, att2, def1, def2)


                prediksi = model.predict([[hp1, hp2, att1, att2, def1, def2, spatt1, spatt2, spdef1, spdef1, speed1, speed2]])
                proba = model.predict_proba([[hp1, hp2, att1, att2, def1, def2, spatt1, spatt2, spdef1, spdef1, speed1, speed2]])
                maxproba = proba[0].max()*100

                if prediksi[0] == 1:
                    hasilpred = nama2
                else:
                    hasilpred = nama

                # print(hasilpred)


                # Plot =====================
                listnama = [nama, nama2]

                listHP = []
                listAttack = []
                listDef = []
                listSpatck = []
                listspdef = []
                listspeed = []

                for i in listnama:
                    listHP.append(db['HP'][db['Name']==i].values[0])
                for i in listnama:
                    listAttack.append(db['Attack'][db['Name']== i].values[0])
                for i in listnama:
                    listDef.append(db['Defense'][db['Name']== i].values[0])
                for i in listnama:
                    listSpatck.append(db['Sp. Atk'][db['Name']== i].values[0])
                for i in listnama:
                    listspdef.append(db['Sp. Def'][db['Name']== i].values[0])
                for i in listnama:
                    listspeed.append(db['Speed'][db['Name']== i].values[0])

                plt.clf()
                plt.figure(figsize=(10, 6))

                plt.subplot(161)
                plt.bar(listnama, listHP, color='br')
                plt.xticks(rotation=90)
                plt.title('HP')

                plt.subplot(162)
                plt.bar(listnama, listAttack, color='br')
                plt.xticks(rotation=90)
                plt.title('Attack')

                plt.subplot(163)
                plt.bar(listnama, listDef, color='br')
                plt.xticks(rotation=90)
                plt.title('Defense')

                plt.subplot(164)
                plt.bar(listnama, listSpatck, color='br')
                plt.xticks(rotation=90)
                plt.title('Sp Attack')

                plt.subplot(165)
                plt.bar(listnama, listspdef, color='br')
                plt.xticks(rotation=90)
                plt.title('Sp Defense')

                plt.subplot(166)
                plt.bar(listnama, listspeed, color='br')
                plt.xticks(rotation=90)
                plt.title('Speed')


                xy = random.randint(10000, 9999999)
                listplot = os.listdir('./storage')
                aa = str(len(listplot) + 1) + '_' + str(xy) + '.jpg'

                plt.savefig('storage/%s' % aa)

                return render_template('profilepokemon.html', a1=nama, a2=nama2, zz=aa,  e=foto2, f=foto1, p=hasilpred, prob=maxproba)

        except():
            return redirect(url_for('error'))

    except():
        return redirect(url_for('error'))


@app.route('/plotku/<path:yy>')                                 # nama path untuk diakses dari web
def plotku(yy):
    return send_from_directory('storage', yy)

@app.route('/error')
def error():
    return render_template('pokemonerror.html')



if __name__ == '__main__':
    app.run(debug=True)
