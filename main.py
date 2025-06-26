from flask import Flask, render_template,request, jsonify
from Agents_IA import executar_consulta
import json


# Iniciando o APP dentro do Flask
app = Flask(__name__)

# Criando a Rota para a Função da IA 
@app.route("/", methods=['GET','POST'])
def index():
    
    artigos =[]
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        resultado_json = executar_consulta(pergunta = pergunta)
        artigos = json.loads(resultado_json)
    return render_template('index.html', artigos = artigos)


# Função para Chamar o Flask
if __name__ == "__main__":
    app.run(debug=True)