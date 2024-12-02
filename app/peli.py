from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)


yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Ruut@sara',
         autocommit=True
         )



def hae_kentta_icao_koodilla(icao_koodi):

    kursori = yhteys.cursor()
    kursori.execute("SELECT name, municipality FROM airport WHERE ident = %s", (icao_koodi,))
    tulos = kursori.fetchone()
    kursori.close()
    yhteys.close()

    if tulos:
        return {"ICAO": icao_koodi, "Name": tulos[0], "Municipality": tulos[1]}
    else:

        return {"ICAO": icao_koodi, "Name": "", "Municipality": ""}



@app.route('/kenttä/<string:icao_koodi>', methods=['GET'])
def hae_kentta(icao_koodi):

    kentta_tiedot = hae_kentta_icao_koodilla(icao_koodi.upper())
    return jsonify(kentta_tiedot)


if __name__ == '__main__':
    app.run(port=3000)
