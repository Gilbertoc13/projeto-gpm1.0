import unittest
from unittest.mock import patch
from app import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_valido(self):
        with self.app as client:
            # Simulando o envio do formulário com dados corretos
            response = client.post('/login', data={'email': 'teste@teste.com', 'senha': 'senha123'}, follow_redirects=True)
            self.assertIn(b'Login realizado com sucesso!', response.data)

    def test_login_invalido(self):
        with self.app as client:
            # Simulando o envio do formulário com dados incorretos
            response = client.post('/login', data={'email': 'nao_existe@teste.com', 'senha': 'senha_incorreta'}, follow_redirects=True)
            self.assertIn('E-mail ou senha inválidos!', response.data)

if __name__ == '__main__':
    unittest.main()
