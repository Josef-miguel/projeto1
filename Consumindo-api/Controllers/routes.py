import urllib.request, json
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = "c6f8ab23618b3fe3a31460aa5d9b8122"  # coloque sua chave aqui

@app.route('/apifilmes', methods=['GET', 'POST'])
@app.route('/apifilmes/<int:id>', methods=['GET','POST'])
def apifilmes(id=None):
    urlAPI = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=pt-BR'
    response = urllib.request.urlopen(urlAPI)
    apiData = response.read()
    listaFilmes = json.loads(apiData)["results"]  # a lista de filmes vem dentro de "results"

    if id:
        # busca detalhes do filme específico
        urlAPI_detalhe = f'https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=pt-BR'
        responseDetalhe = urllib.request.urlopen(urlAPI_detalhe)
        filmeInfo = json.loads(responseDetalhe.read())
        if filmeInfo:
            return render_template('filmeinfo.html', filmeInfo=filmeInfo)
        else:
            return f'Filme com a ID {id} não foi encontrado.'
    
    return render_template('apifilmes.html', listaFilmes=listaFilmes)
