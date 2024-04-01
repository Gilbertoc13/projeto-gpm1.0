
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
usuarios_collection = db['usuarios']

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

if __name__ == '__main__':
    app.run(debug=True)