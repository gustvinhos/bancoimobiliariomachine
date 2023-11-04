import pandas as pd
import sqlite3
import streamlit as st
import time



class Login_class:
    def __init__(self):
        pass

    def create_user(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        with st.form(key='form1', clear_on_submit=True):
            st.header("Cadastro")
            
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            submitted = st.form_submit_button("Cadastrar")
            
            if submitted:
                if len(cpf) != 11:
                    st.warning("CPF inválido")
                else:
                    c.execute("""select * from jogadores where cpf = ?""", (cpf,))
                    user = c.fetchall()

                    if len(user) > 0:
                        st.warning("Usuário já cadastrado")
                    else:
                        c.execute("""INSERT INTO jogadores (nome, cpf, email, senha, status) VALUES (?,?,?,?,?)""", (nome, cpf, email, senha, "Fora de jogo"))
                        conn.commit()
                        c.close()
                        conn.close()
                        st.success("Usuário cadastrado com sucesso")
                        time.sleep(1)
                        return user
                            

    def login(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        with st.form(key='form2'):
            st.header("Login")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")

            if st.form_submit_button("Login"):
                c.execute("""select * from jogadores where email = ? and senha = ?""", (email, senha))
                user = c.fetchall()

                if len(user) > 0:
                    st.success("Logado com sucesso")
                    st.session_state['user'] = user[0][0]
                    print(st.session_state['user'])
                    st.rerun()
                else:
                    st.warning("Email ou senha incorretos")
                    return False

    
    




