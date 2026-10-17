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

    def test_pagina_inicial(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_criar_e_excluir_nota(self):
        response = self.app.post('/criar', data=dict(
            titulo='Nota Teste',
            conteudo='Conteúdo Teste',
            categoria_id=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nota Teste', response.data)

        # Excluir nota ID 1
        response = self.app.post('/excluir/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()