from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)


@app.route('/')
@app.route('/page_1.html')
def home_page():
    return render_template("page_1.html")


@app.route('/HTML.html', methods=['POST', 'GET'])
def database():
    # de knoppen op de website geven een "True" mee aan het python script
    # zodat deze weet welke queries gemaakt moeten worden.
    # ook krijgt het script een string binnen waarop gezocht moet worden
    filter_text = request.values.get("input", "")
    ID = request.values.get("ID", "False")
    description = request.values.get("Description", "False")
    score = request.values.get("Score", "False")
    taxonomy = request.values.get("Taxonomy", "False")

    # de waarden van de knoppen worden meegegeven
    data = connector(filter_text, ID, description, score, taxonomy)
    if request.method == 'GET':
        return render_template("HTML.html", data=data)


def connector(filter_text, ID, description, score, taxonomy):
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="flezi@hannl-hlo-bioinformatica-mysqlsrv",
        db="flezi",
        passwd="Tutorgroep4HYL")

    # de basis van de query
    exec_string = "SELECT * FROM result join taxonomy on result.taxonomy_id=taxonomy.taxonomy_id"
    # waarneer de base_extend op True staat zal er op een andere manier
    # toegevoegd worden aan de query
    base_extend = False

    # als de ID knop op true staat word er een zoek query gemaakt voor de
    # gewenste zoekterm
    if ID == "True":
        # afhankelijk van of er al wat in de query staat word die op een
        # andere manier opgebouwd.
        if base_extend:
            exec_string += " or ID = " + filter_text
        if not base_extend:
            exec_string += " where ID = " + filter_text
        # de base extend word op true gezet zodat de query anders opgebouwd
        # zal worden
        base_extend = True

    # als de description knop op true staat word er een zoek query gemaakt voor
    # de gewenste zoekterm
    if description == "True":
        if base_extend:
            exec_string += "or description like '%" + filter_text + "%'"
        if not base_extend:
            exec_string += " where description like '%" + filter_text + "%'"
        base_extend = True

    # als de score knop op true staat word er een zoek query gemaakt voor
    # de gewenste zoekterm
    if score == "True":
        if base_extend:
            exec_string += " or Score = " + filter_text
        if not base_extend:
            exec_string += " where Score = " + filter_text
        base_extend = True

    # als de taxonomy knop op true staat word er een zoek query gemaakt voor
    # de gewenste zoekterm
    if taxonomy == "True":
        if base_extend:
            exec_string += " or Naam like '%" + filter_text + "%'"
        if not base_extend:
            exec_string += " where Naam like '%" + filter_text + "%'"
        base_extend = True

    cursor = conn.cursor()
    cursor.execute(exec_string)
    data = cursor.fetchall()
    conn.close()
    cursor.close()
    return data


if __name__ == '__main__':
    app.run(debug=True)
