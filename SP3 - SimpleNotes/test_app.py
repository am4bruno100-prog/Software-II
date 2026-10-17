import unittest
import os
import app

class SimpleNotesTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.DATABASE = 'test_database.db'
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        if os.path.exists('test_database.db'):
            os.remove('test_database.db')

    def test_1_pagina_inicial(self):
        """Teste 1: Verifica se a página inicial (listagem de notas) carrega com sucesso (HTTP 200)."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SimpleNotes', response.data)

    def test_2_criar_nota(self):
        """Teste 2: Verifica a criação de uma nova nota e redirecionamento para a página inicial."""
        response = self.app.post('/criar', data=dict(
            titulo='Nota de Teste Unico',
            conteudo='Conteudo da nota para validar insercao',
            categoria_id=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nota de Teste Unico', response.data)

    def test_3_filtrar_por_categoria(self):
        """Teste 3: Verifica se a filtragem de notas por categoria funciona corretamente."""
        # Cria uma nota na categoria 2 (Financeiro)
        self.app.post('/criar', data=dict(
            titulo='Pagar Fatura',
            conteudo='Verificar valor da fatura',
            categoria_id=2
        ), follow_redirects=True)
        
        # Acessa a pagina filtrando pela categoria 2
        response = self.app.get('/?categoria_id=2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pagar Fatura', response.data)

    def test_4_editar_nota(self):
        """Teste 4: Verifica a alteracao/edicao de uma nota existente."""
        # Cria a nota inicial
        self.app.post('/criar', data=dict(
            titulo='Titulo Original',
            conteudo='Conteudo Original',
            categoria_id=1
        ), follow_redirects=True)
        
        # Edita a nota de ID 1
        response = self.app.post('/editar/1', data=dict(
            titulo='Titulo Alterado',
            conteudo='Conteudo Atualizado com Sucesso',
            categoria_id=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Titulo Alterado', response.data)
        self.assertIn(b'Conteudo Atualizado com Sucesso', response.data)

    def test_5_excluir_nota(self):
        """Teste 5: Verifica a exclusao de uma nota do banco de dados."""
        # Cria nota a ser excluida
        self.app.post('/criar', data=dict(
            titulo='Nota Para Deletar',
            conteudo='Esta nota sera removida',
            categoria_id=1
        ), follow_redirects=True)
        
        # Executa a exclusao da nota ID 1
        response = self.app.post('/excluir/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Nota Para Deletar', response.data)

if __name__ == '__main__':
    unittest.main()
