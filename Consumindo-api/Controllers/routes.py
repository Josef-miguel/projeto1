import urllib.request, json
from flask import render_template, request, url_for, redirect
from flask import Blueprint, render_template



API_KEY = "c6f8ab23618b3fe3a31460aa5d9b8122"
def init_app(app):
 @app.route('/')
 def home():
    return render_template('home.html')

 @app.route('/apifilmes', methods=['GET', 'POST'])
 @app.route('/apifilmes/<int:id>', methods=['GET', 'POST'])
 def apifilmes(id=None):
    urlAPI = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=pt-BR'
    response = urllib.request.urlopen(urlAPI)
    apiData = response.read()
    listaFilmes = json.loads(apiData)["results"]

    if id:
        urlAPI_detalhe = f'https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=pt-BR'
        responseDetalhe = urllib.request.urlopen(urlAPI_detalhe)
        filmeInfo = json.loads(responseDetalhe.read())
        return render_template('filmeinfo.html', filmeInfo=filmeInfo)

    return render_template('apifilmes.html', listaFilmes=listaFilmes)
