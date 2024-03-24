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




@app.route('/')
def index():
    return render_template('login.html')

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if senha != confirmar_senha:
            return "As senhas não coincidem!"

        if usuarios_collection.find_one({'email': email}):
            return "E-mail já cadastrado!"

        senha_criptografada = bcrypt.generate_password_hash(senha).decode('utf-8')
        novo_usuario = {'nome': nome, 'email': email, 'senha': senha_criptografada}
        usuarios_collection.insert_one(novo_usuario)

        return redirect(url_for('sucesso', mensagem='Cadastro realizado com sucesso!'))

    return redirect(url_for('index'))


    

@app.route('/sucesso')
def sucesso():
    mensagem = request.args.get('mensagem')
    return render_template('sucesso.html', mensagem=mensagem)
    
   

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
       email= request.form['email']
       senha = request.form['senha']

       usuario = usuarios_collection.find_one({'email': email})

       if usuario and Bcrypt.check_password_hash(usuario['senha'],senha):
           session['usuario_id'] = str(usuario['_id'])
           return redirect(url_for('sucesso'))
       else:
           return 'E-mail ou senha invalidos!'
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

