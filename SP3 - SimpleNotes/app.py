import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', mode='r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

@app.route('/')
def index():
    categoria_id = request.args.get('categoria_id')
    conn = get_db_connection()
    categorias = conn.execute('SELECT * FROM categoria').fetchall()
    
    if categoria_id:
        notas = conn.execute('''
            SELECT n.*, c.nome as categoria_nome 
            FROM nota n JOIN categoria c ON n.categoria_id = c.id 
            WHERE n.categoria_id = ? 
            ORDER BY n.data_criacao DESC
        ''', (categoria_id,)).fetchall()
    else:
        notas = conn.execute('''
            SELECT n.*, c.nome as categoria_nome 
            FROM nota n JOIN categoria c ON n.categoria_id = c.id 
            ORDER BY n.data_criacao DESC
        ''', ()).fetchall()
        
    conn.close()
    return render_template('index.html', notas=notas, categorias=categorias, categoria_selecionada=int(categoria_id) if categoria_id else None)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    conn = get_db_connection()
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        categoria_id = request.form['categoria_id']
        
        conn.execute('INSERT INTO nota (titulo, conteudo, categoria_id) VALUES (?, ?, ?)',
                     (titulo, conteudo, categoria_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    categorias = conn.execute('SELECT * FROM categoria').fetchall()
    conn.close()
    return render_template('form.html', categorias=categorias, nota=None)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    nota = conn.execute('SELECT * FROM nota WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        categoria_id = request.form['categoria_id']
        
        conn.execute('UPDATE nota SET titulo = ?, conteudo = ?, categoria_id = ? WHERE id = ?',
                     (titulo, conteudo, categoria_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    categorias = conn.execute('SELECT * FROM categoria').fetchall()
    conn.close()
    return render_template('form.html', categorias=categorias, nota=nota)

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM nota WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)