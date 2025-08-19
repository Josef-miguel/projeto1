import urllib.request
import json
from flask import render_template, request, url_for, redirect

API_KEY = "c6f8ab23618b3fe3a31460aa5d9b8122"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fazer_requisicao(endpoint):
    """Função utilitária para fazer requisições à API do TMDB"""
    url = f"{TMDB_BASE_URL}{endpoint}?api_key={API_KEY}&language=pt-BR"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())

def buscar_generos():
    dados = fazer_requisicao("/genre/movie/list")
    return {genero["id"]: genero["name"] for genero in dados["genres"]}

def init_app(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/apifilmes', methods=['GET', 'POST'])
    @app.route('/apifilmes/<int:id>', methods=['GET', 'POST'])
    def apifilmes(id=None):
        if id:
   
            filmeInfo = fazer_requisicao(f"/movie/{id}")

            
            creditsData = fazer_requisicao(f"/movie/{id}/credits")
            diretor = next((p for p in creditsData["crew"] if p["job"] == "Director"), None)

          
            videosData = fazer_requisicao(f"/movie/{id}/videos")
            trailer = next((v for v in videosData["results"]
                            if v["type"] == "Trailer" and v["site"] == "YouTube"), None)

            return render_template("filmeinfo.html", filmeInfo=filmeInfo, diretor=diretor, trailer=trailer)

        
        generos_dict = buscar_generos()
        listaFilmes = []


        for pagina in range(1, 2):
            endpoint = f"/movie/popular&page={pagina}"
            url = f"{TMDB_BASE_URL}/movie/popular?api_key={API_KEY}&language=pt-BR&page={pagina}"
            with urllib.request.urlopen(url) as response:
                apiData = json.loads(response.read())
                filmes = apiData["results"]

                for filme in filmes:
                    ids_generos = filme.get("genre_ids", [])
                    filme["genres"] = [generos_dict.get(id_gen, "Desconhecido") for id_gen in ids_generos]
                    listaFilmes.append(filme)

        return render_template("apifilmes.html", listaFilmes=listaFilmes)
