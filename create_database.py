import sqlite3
import streamlit as st

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    vencedor_id TEXT,
    valor_monetario REAL ,
    status TEXT,
    valor_inicial INT
             )
    """
             
)

print("Table created successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    status TEXT NOT NULL,
    id_jogo_atual INTEGER
        )
    """
)

print("Table created successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS jogadores_jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER NOT NULL,
    jogo_id INTEGER NOT NULL,
    saldo REAL NOT NULL,
    qtd_sortes INTEGER NOT NULL,
    qtd_azar INTEGER NOT NULL,
    qtd_transacoes INTEGER NOT NULL
                          )
    """
)

print("Table created successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id_pagante INTEGER NOT NULL,
    jogador_id_recebedor INTEGER NOT NULL,
    jogo_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL
                          )
    """
)

conn.execute("""CREATE TABLE IF NOT EXISTS propriedades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_propriedade TEXT NOT NULL,
    modelo_jogo TEXT NOT NULL,
    valor_compra REAL NOT NULL,
    valor_aluguel REAL NOT NULL,
    valor_casa REAL NOT NULL,
    valor_hotel REAL NOT NULL, 
    cor TEXT NOT NULL
                          )
    """
)




conn.close()


