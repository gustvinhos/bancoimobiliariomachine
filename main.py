import streamlit as st
import pandas as pd
import numpy as np
from login import Login_class
import sqlite3
from adm_jogos import Jogos
from carteira import Carteira
import time


def tela_inicial():
    #conectar no banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()




    #verificar os st.session_state['user'] e st.session_state['jogo_id']
    c.execute("""select * from jogadores where id = ?""", (st.session_state['user'],))
    info = c.fetchall()
    status = info[0][5]
    if status == "Em jogo":
        st.session_state['jogo_id'] = info[0][6]
    elif status == "Fora de jogo":
        st.session_state['jogo_id'] = None


    with st.sidebar:
        choice = st.selectbox("Select", ["Em jogo", "Transações", "Novo Jogo", "Finalizar Jogo"])
        #criar um botão para resetart todas as bases exceto a de jogadores
        if button := st.button("Resetar"):
            if button:
                conn.execute("""DELETE FROM jogos""")
                conn.execute("""DELETE FROM jogadores_jogos""")
                conn.execute("""DELETE FROM transacoes""")
                #apagar os dados das colunas de status e id_jogo_atual da tabela jogadores
                conn.execute("""UPDATE jogadores SET status = ?, id_jogo_atual = ?""", ("Fora de jogo", None))
                conn.commit()
                st.success("Bases resetadas com sucesso")
                st.rerun()

        if st.button("Logout"):
            del st.session_state['user']
            st.rerun()

    if choice == "Em jogo":
        #buscar o nome do jogador
        c.execute("""select * from jogadores where id = ?""", (st.session_state['user'],))
        info = c.fetchall()
        nome = info[0][1]
        nome = nome.split(" ")[0]
        st.subheader(f"Olá, {nome}")
        #verificar o status do jogador
        status = info[0][5]
        if status == "Fora de jogo":
            st.write("Você não está em nenhum jogo no momento")   

        elif status == "Em jogo":
            
            submenu = st.sidebar.selectbox("Selecione:", ["Carteira", "Comprar Propriedade", "Comprar Casas", "Transações"])

            if submenu == "Carteira":
                carteira = Carteira()
                saldo = carteira.ver_saldo()
                transacoes = carteira.form_transacoes()

                if st.button("Atualizar histórico"):
                    carteira.historico()
                



   

        





    if choice == "Novo Jogo":
        jogo = Jogos()
        jogo.criar_jogo()

    if choice == "Finalizar Jogo":
        jogo = Jogos()
        jogo.finalizar_jogo()





        

def main():

    if 'user' not in st.session_state:
        
        choice = st.selectbox("Selecione:", ["Login", "Cadastro"])
        print(st.experimental_get_query_params())

        if choice == "Login":
            login = Login_class()
            login.login()
        elif choice == "Cadastro":
            login = Login_class()
            login.create_user()



    elif 'user' in st.session_state:
        tela_inicial()






main()

