from flask import request, jsonify, Blueprint
from dotenv import load_dotenv
import requests
import os

load_dotenv()
api_key = os.getenv('TMDB_KEY')
tmdb_bp = Blueprint("tmdb_bp", __name__)

@tmdb_bp.route("/tmdb/logo", methods=["GET"])
def test_route_tmdb():
    tipo = request.args.get('tipo')
    id = request.args.get('id')

    url = f"https://api.themoviedb.org/3/{tipo}/{id}/images"
    parametros = {'api_key': api_key}
    response = requests.get(url, params=parametros)

    if response.status_code == 200:
        data = response.json()
        pt_item = next((item for item in data.get('logos', []) if item.get('iso_639_1') == 'pt'), None)
        selected_item = pt_item or next((item for item in data.get('logos', []) if item.get('iso_639_1') == 'en'), None)
        url = f"https://image.tmdb.org/t/p/original{selected_item.get('file_path')}"
        return jsonify({"logo": url})
    else:
        return jsonify({"error": "Não foi possível obter o logo do TMDB"}), response.status_code