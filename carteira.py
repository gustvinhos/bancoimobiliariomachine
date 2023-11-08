import sqlite3
import streamlit as st
import time
import locale
import pandas as pd


class Carteira:
    def __init__(self):
        #pegar o valor inicial do jogo
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

        #formatar o valor para R$ e separador de milhar
        
        
        saldo_formatado = saldo_formatado.replace(",00", "")

    # HTML para o conteúdo
        html_content = """
            <div class="saldo-container">
                <h2 class="saldo-title">Saldo Atual:</h2>
                <p class="saldo-amount">💰 {}</p>
            </div>
        """.format(saldo_formatado)

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
        
        jogador = st.number_input("Jogador", key='jogador_recebedor', on_change=self.buscar_jogador(), value=0, step=1, format="%d")
        valor = st.number_input("Valor",value=0, step=1000, format="%i")
        #mostrar valor formatado com R$ e separador de milhar
        valor_formatado = valor_formatado.replace(",00", "")
        st.write(valor_formatado)



        col1, col2, col3, col4 = st.columns(4)
        with col1:
            enviar = st.button("Enviar ⛔", use_container_width=True)
            
        with col2:
            #conectar no banco
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            #buscar o valor inicial do jogo atual
            c.execute("""select * from jogos where id = ?""", (st.session_state['jogo_id'],))
            info = c.fetchall()
            valor_inicial_jogo = info[0][5]
            if valor_inicial_jogo > 1000000:
                denominator = 100000
            else:
                denominator = 10000

            valor_inicial_jogo = valor_inicial_jogo/10
            valor_inicial_jogo = round(valor_inicial_jogo / denominator) * denominator
            valor_inicial_formatado = valor_inicial_jogo
            #formatar o valor para R$ e separador de milhar

            valor_inicial_jogo = valor_inicial_jogo.replace(",00", "")


            receba_text = "Receber " + str(valor_inicial_jogo) + " 💰"
            receba_2k = st.button(receba_text, use_container_width=True)
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
            saldo += valor_inicial_formatado
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

    def historico(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""select * from transacoes where jogador_id_pagante = ? or jogador_id_recebedor = ?""", (st.session_state['user'], st.session_state['user']))
        info = c.fetchall()
        #pegar o id dos jogadores tanto pagante quanto recebedor e substituir pelo nome
        for i in range(len(info)):
            c.execute("""select * from jogadores where id = ?""", (info[i][1],))
            info_pagante = c.fetchall()
            info[i] = list(info[i])
            info[i][1] = info_pagante[0][1]
            c.execute("""select * from jogadores where id = ?""", (info[i][2],))
            info_recebedor = c.fetchall()
            info[i][2] = info_recebedor[0][1]
        #converter a lista de tuplas para dataframe
        df = pd.DataFrame(info, columns=['id', 'jogador_id_pagante', 'jogador_id_recebedor', 'jogo_id', 'valor', 'tipo', 'data', 'hora'])
        #pegar só algumas colunas do df
        df = df[['jogador_id_pagante', 'jogador_id_recebedor', 'valor', 'tipo', 'hora']]
        #renomear as colunas
        df.columns = ['Pagante', 'Recebedor', 'Valor', 'Tipo', 'Hora']
        df = df.sort_values(by=['Hora'], ascending=False)
       
        df['Valor'] = df['Valor'].apply(lambda x: x.replace(",00", ""))
        st.dataframe(df, hide_index=True)
        c.close()





            
        

        
        
        