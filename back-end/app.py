
from flask import Flask, render_template, request, redirect, url_for, session
#banco de dados para importar
from pymongo import MongoClient
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
bcrypt = Bcrypt(app)

#configurações do banco de dados
Mongo_URL= 'mongodb://localhost:27017/'
DB_name = 'gpmDB'

client = MongoClient(Mongo_URL)
db = client[DB_name]
#criação da coleção para usuarios(Login\Cadastro)
usuarios_collection = db['usuarios']
#criação da coleção filmes para usuario adicionar a sua lista
filmes_collection = db['filmes']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = usuarios_collection.find_one({'email': email})

        if usuario and bcrypt.check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = str(usuario['_id'])
            return 'Login realizado com sucesso!'
        else:
            return 'E-mail ou senha inválidos!'

    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
        novo_usuario = {'email': email, 'senha': hashed_senha}
        usuarios_collection.insert_one(novo_usuario)

        return 'Usuário cadastrado com sucesso!'

    return render_template('cadastro.html')

@app.route('/')
def index():
    filmes = filmes_collection.find()
    return render_template('filmes.html',filmes = filmes)

@app.route('/assistir/<filme_id>', methods=['POST'])
def assistir_filme(filme_id):
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


def get_filmes_vistos(usuario_id):
    usuario = usuarios_collection.find_one({'_id': usuario_id})
    if usuario:
        filmes_vistos = usuario.get('filmes_vistos', []) 
        return filmes_vistos
    else:
        return []
    

@app.route('/lista', methods=['GET'])
def lista():
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        filmes_vistos = get_filmes_vistos(usuario_id)
        if filmes_vistos:
            filmes_info = []  
            for filme_id in filmes_vistos:
                filme = filmes_collection.find_one({'_id': filme_id})
                if filme:
                    filmes_info.append(filme)  
            return render_template('lista.html', filmes=filmes_info)
        else:
            return 'Nenhum filme foi marcado como assistido ainda.'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)