from flask import Flask, request, send_file
from scraper import scrape_to_csv, generer_nom_fichier
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
CORS(app)


@app.route('/generate-csv', methods=['POST'])
def generate_csv():
    data = request.json
    url = data['url']

    # Génère le nom du fichier basé sur l'URL
    nom_fichier = generer_nom_fichier(url)
    # Chemin complet du fichier dans le dossier 'pages'
    dossier = 'pages'
    csv_path = os.path.join(dossier, nom_fichier)

    # Assurez-vous que le dossier 'pages' existe
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    # Appel à la fonction de scraping pour générer le CSV
    scrape_to_csv(url, csv_path)

    # Retourne le fichier CSV généré
    return send_file(csv_path, as_attachment=True, download_name=nom_fichier)


if __name__ == '__main__':
    app.run(debug=True)

