DROP TABLE IF EXISTS nota;
DROP TABLE IF EXISTS categoria;

CREATE TABLE categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE nota (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categoria (id) ON DELETE CASCADE
);

INSERT INTO categoria (nome) VALUES ('Faculdade'), ('Financeiro'), ('Pet'), ('Pessoal');