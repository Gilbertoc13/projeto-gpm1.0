import unittest
from app import app, usuarios_collection

class TestCadastro(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_cadastrar_usuario(self):
        with self.app as client:
            # Simulando o envio do formulário com dados corretos
            response = client.post('/cadastrar', data={'nome': 'Teste', 'email': 'teste@teste.com', 'senha': 'senha123', 'confirmar_senha': 'senha123'}, follow_redirects=True)
            self.assertIn(b'Cadastro realizado com sucesso!', response.data)

            # Verifica se o usuário foi adicionado à coleção
            self.assertTrue(any(usuario['email'] == 'teste@teste.com' for usuario in usuarios_collection))

    def test_cadastrar_usuario_senhas_diferentes(self):
        with self.app as client:
            # Simulando o envio do formulário com senhas diferentes
            response = client.post('/cadastrar', data={'nome': 'Teste', 'email': 'teste2@teste.com', 'senha': 'senha123', 'confirmar_senha': 'outrasenha'}, follow_redirects=True)
            self.assertIn('As senhas não coincidem!', response.data)

            # Verifica se o usuário não foi adicionado à coleção
            self.assertFalse(any(usuario['email'] == 'teste2@teste.com' for usuario in usuarios_collection))

if __name__ == '__main__':
    unittest.main()
