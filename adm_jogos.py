import sqlite3
import streamlit as st
import time
import pandas as pd


class Jogos:

    def __init__(self):
        pass

    def criar_jogo(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #verificar se o usuário está em algum jogo
        c.execute("""select * from jogadores where id = ?""", (st.session_state['user'],))
        info = c.fetchall()
        status = info[0][5]
        if status == "Em jogo":
            st.warning("Você já está em um jogo")
        elif status == "Fora de jogo":
            with st.form(key='form1', clear_on_submit=True):
                st.header("Criar jogo")
                
                valor_inicial = st.number_input("Valor Inicial", min_value=0.0, step=0.01)
                #selecionar os jogadores que vão participar do jogo
                c.execute("""select * from jogadores""")
                jogadores = c.fetchall()
                jogadores = [jogador[1] for jogador in jogadores]
                jogadores = st.multiselect("Jogadores", jogadores)
                submitted = st.form_submit_button("Criar jogo")
                
                if submitted:
                    c.execute("""INSERT INTO jogos (date) VALUES (?)""", (time.strftime("%d/%m/%Y"),))
                    conn.commit()
                    #buscar o id do último jogo criado
                    c.execute("""select * from jogos""")
                    jogos = c.fetchall()
                    id_jogo = jogos[-1][0]
                    #buscar o id dos jogadores selecionados
                    for jogador in jogadores:
                        c.execute("""select * from jogadores where nome = ?""", (jogador,))
                        jogador_id = c.fetchall()
                        jogador_id = jogador_id[0][0]
                        #verificar se o jogador já está em algum jogo
                        c.execute("""select * from jogadores where id = ?""", (jogador_id,))
                        jogador_info = c.fetchall()
                        status = jogador_info[0][5]
                        if status == "Em jogo":
                            st.warning(f"O jogador {jogador} já está em um jogo")
                        elif status == "Fora de jogo":
                            c.execute("""UPDATE jogadores SET status = ?, id_jogo_atual = ? WHERE id = ?""", ("Em jogo", id_jogo, jogador_id))
                            c.execute("""INSERT INTO jogadores_jogos (jogador_id, jogo_id, saldo, qtd_sortes, qtd_azar, qtd_transacoes) VALUES (?,?,?,?,?,?)""", (jogador_id, id_jogo, valor_inicial, 0, 0, 0))
                            st.session_state['jogo_id'] = id_jogo
                            conn.commit()
                    


                    c.close()
                    conn.close()
                    st.success("Jogo criado com sucesso")
                    time.sleep(1)
                    st.rerun()

    def finalizar_jogo(self):
        if st.button("Finalizar jogo"):
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            #buscar o id do jogo atual
            c.execute("""select * from jogadores where id = ?""", (st.session_state['user'],))
            info = c.fetchall()
            id_jogo = info[0][6]
            #pegar o jogador com maior saldo usando pandas
            c.execute("""select * from jogadores_jogos where jogo_id = ?""", (st.session_state['jogo_id'],))
            info = c.fetchall()
            df = pd.DataFrame(info, columns=['id', 'jogador_id', 'jogo_id', 'saldo', 'qtd_sortes', 'qtd_azar', 'qtd_transacoes'])
            df = df.sort_values(by=['saldo'], ascending=False)
            vencedor_id = df.iloc[0]['jogador_id']

            #atualizar o status de todos os jogadores para fora de jogo
            c.execute("""UPDATE jogadores SET status = ?, id_jogo_atual = ?""", ("Fora de jogo", None))
            #atualizar o status do jogo
            c.execute("""UPDATE jogos SET status = ?, vencedor_id = ? WHERE id = ?""", ("Finalizado", vencedor_id, st.session_state['jogo_id']))
            conn.commit()
            #pegar o nome do vencedor para mostrar na tela
            c.execute("""select * from jogadores where id = ?""", (vencedor_id,))
            info = c.fetchall()
            vencedor = info[0][1]
            conn.close()


            st.success("Jogo finalizado com sucesso e o vencedor foi:",vencedor)
            

