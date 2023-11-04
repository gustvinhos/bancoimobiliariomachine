import sqlite3
import streamlit as st
import time


class Carteira:
    def __init__(self):
        pass

    def saldo(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print(st.session_state['jogo_id'])
#se o id do jogo atual não estiver na sessão, buscar o id do jogo atual do jogador
        if 'jogo_id' not in st.session_state:
            c.execute("""select * from jogadores where id = ?""", (st.session_state['user'],))
            info = c.fetchall()
            jogo_id = info[0][7]
            st.session_state['jogo_id'] = jogo_id

        #buscar o saldo do jogador no jogo atual
        c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (st.session_state['user'], st.session_state['jogo_id']))
        info = c.fetchall()
        saldo = info[0][3]
        return saldo

        


    
    def enviar_dinheiro(self, valor, jogador):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (st.session_state['user'], st.session_state['jogo_id']))
        info = c.fetchall()
        saldo = info[0][3]

        if valor > saldo:
            st.warning("Saldo insuficiente")
            return st.error("Transação não realizada")
        else:
            #verifica se o jogador que vai receber o dinheiro está no jogo e existe
            c.execute("""select * from jogadores where id = ?""", (jogador,))
            jogador_info = c.fetchall()
            if len(jogador_info) == 0:
                st.warning("Jogador não encontrado")
                return st.error("Transação não realizada")
            else:
                
                #atualizar o saldo do jogador que enviou o dinheiro
                saldo -= valor
                c.execute("""UPDATE jogadores_jogos SET saldo = ? WHERE jogador_id = ? and jogo_id = ?""", (saldo, st.session_state['user'], st.session_state['jogo_id']))
                #atualizar o saldo do jogador que recebeu o dinheiro
                c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (jogador, st.session_state['jogo_id']))
                info = c.fetchall()
                saldo = info[0][3]
                saldo += valor
                c.execute("""UPDATE jogadores_jogos SET saldo = ? WHERE jogador_id = ? and jogo_id = ?""", (saldo, jogador, st.session_state['jogo_id']))
                #atualizar a quantidade de transações do jogador que enviou o dinheiro
                conn.commit()
                c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (st.session_state['user'], st.session_state['jogo_id']))
                info = c.fetchall()
                qtd_transacoes = info[0][6]
                qtd_transacoes += 1
                #inserir no banco de dados a transação
                c.execute("""INSERT INTO transacoes (jogador_id_pagante, jogador_id_recebedor, jogo_id, valor, tipo, data, hora) VALUES (?,?,?,?,?,?,?)""", (st.session_state['user'], jogador, st.session_state['jogo_id'], valor, "envio", time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))

                conn.commit()
                c.close()
                st.success("Transação realizada com sucesso")
                time.sleep(1)


    def buscar_jogador(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        if 'jogador_recebedor' not in st.session_state:
            st.session_state['jogador_recebedor'] = 0
        c.execute("""select * from jogadores where id = ?""", (st.session_state['jogador_recebedor'],))
        jogador_info = c.fetchall()
        if len(jogador_info) == 0:
            return st.write("Quem recebe: Jogador não encontrado ❌ ")
        else:
            return st.write("Quem recebe: ", jogador_info[0][1], " ✅")


    def ver_saldo(self):
        #mostrar o saldo atual do jogador
        carteira = Carteira()
        saldo = carteira.saldo()

        
        #colocar pontuação de milhar
        saldo = str(saldo)
        saldo = saldo.split(".")
        saldo = saldo[0]
        saldo = saldo[::-1]
        saldo = saldo.replace(".", ",")
        saldo = saldo[::-1]

    # HTML para o conteúdo
        html_content = """
            <div class="saldo-container">
                <h2 class="saldo-title">Saldo Atual:</h2>
                <p class="saldo-amount">💰 R$ {}</p>
            </div>
        """.format(saldo)

        # CSS para o estilo
        css_style = """
            <style>
            .saldo-container {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
            }

            .saldo-title {
                color: #0073e6;
            }

            .saldo-amount {
                font-size: 24px;
                font-weight: bold;
                color: black;
            }
            </style>
        """

        # Inserir o HTML e o CSS no markdown
        st.markdown(html_content + css_style, unsafe_allow_html=True)


        atualizar_saldo = st.button("Atualizar saldo manualmente")
        if atualizar_saldo:
            self.saldo()


    def form_transacoes(self):

        st.header("Transações")
        
        jogador = st.number_input("Jogador", key='jogador_recebedor', on_change=self.buscar_jogador(), value=None, step=1)
        valor = st.number_input("Valor",value=None, step=500)


        col1, col2, col3, col4 = st.columns(4)
        with col1:
            enviar = st.button("Enviar ⛔", use_container_width=True)
            
        with col2:
            receba_2k = st.button("Receber 2K 💰", use_container_width=True)
        with col3:
            azar = st.button("Azar ⛔", use_container_width=True)
        with col4:
            sorte = st.button("Sorte 💰", use_container_width=True)


        if enviar:
            message = st.empty()
            message.text("Processando transação...")
            self.enviar_dinheiro(valor, jogador)
            message.text("Transação concluída.")



        if receba_2k:
            message = st.empty()
            message.text("Processando transação...")
            #somar 2000 ao saldo do jogador
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (st.session_state['user'], st.session_state['jogo_id']))
            info = c.fetchall()
            saldo = info[0][3]
            saldo += 2000
            c.execute("""UPDATE jogadores_jogos SET saldo = ? WHERE jogador_id = ? and jogo_id = ?""", (saldo, st.session_state['user'], st.session_state['jogo_id']))
            #inserir no banco de dados a transação
            c.execute("""INSERT INTO transacoes (jogador_id_pagante, jogador_id_recebedor, jogo_id, valor, tipo, data, hora) VALUES (?,?,?,?,?,?,?)""", (st.session_state['user'], st.session_state['user'], st.session_state['jogo_id'], 2000, "recebimento", time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
            conn.commit()
            c.close()
            message.text("Transação concluída.")


        if azar:
            message = st.empty()
            message.text("Processando transação...")
            #subtrair o valor digitado do saldo do jogador
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (st.session_state['user'], st.session_state['jogo_id']))
            info = c.fetchall()
            saldo = info[0][3]
            saldo -= valor
            c.execute("""UPDATE jogadores_jogos SET saldo = ? WHERE jogador_id = ? and jogo_id = ?""", (saldo, st.session_state['user'], st.session_state['jogo_id']))
            #inserir no banco de dados a transação
            c.execute("""INSERT INTO transacoes (jogador_id_pagante, jogador_id_recebedor, jogo_id, valor, tipo, data, hora) VALUES (?,?,?,?,?,?,?)""", (st.session_state['user'], st.session_state['user'], st.session_state['jogo_id'], valor, "azar", time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
            conn.commit()
            c.close()
            message.text("Transação concluída.")


        if sorte:
            message = st.empty()
            message.text("Processando transação...")
            #somar o valor digitado do saldo do jogador
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("""select * from jogadores_jogos where jogador_id = ? and jogo_id = ?""", (st.session_state['user'], st.session_state['jogo_id']))
            info = c.fetchall()
            saldo = info[0][3]
            saldo += valor
            c.execute("""UPDATE jogadores_jogos SET saldo = ? WHERE jogador_id = ? and jogo_id = ?""", (saldo, st.session_state['user'], st.session_state['jogo_id']))
            #inserir no banco de dados a transação
            c.execute("""INSERT INTO transacoes (jogador_id_pagante, jogador_id_recebedor, jogo_id, valor, tipo, data, hora) VALUES (?,?,?,?,?,?,?)""", (st.session_state['user'], st.session_state['user'], st.session_state['jogo_id'], valor, "sorte", time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
            conn.commit()
            c.close()
            message.text("Transação concluída.")
            #atualizar o saldo do jogador na tela
            self.saldo()





            
        

        
        
        