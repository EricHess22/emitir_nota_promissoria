import streamlit as st
from streamlit_option_menu import option_menu
import json
import subprocess
import requests
import PyPDF2
import io
import os


# Configuração inicial da página
st.set_page_config(page_title='Emitir Nota Promissória', layout='centered')

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=['Início', 'Nota Promissória em branco','O que é Nota Promissória?', 'Termos de uso'],
        icons=['house','file-earmark', 'question-circle', 'file-text'],
        menu_icon='cast',
        default_index=0,
    )

st.sidebar.divider()
with st.sidebar.expander(":smiley: Apoie para manter este site no ar!", expanded=True):
    st.write('**Chave Pix E-mail:**')
    st.code('emitirnp@gmail.com')
    st.write(':green[**#FazUmPix**]')


#########################################################################
############################## PÁGINA HOME ##############################
#########################################################################

if selected == 'Início':
    #st.header('Emita notas promissórias gratuitamente')
    #st.subheader('Preencha os dados abaixo e emita suas notas promissórias em poucos segundos')

    st.success('Nós nunca armazenamos dados de preenchimento da Nota Promissória :lock:')
    
    # Dados na nota promissória
    st.subheader('Dados da Nota Promissória', anchor=False)
    col1, col2 = st.columns([1, 1])
    quantidade_notas = col1.number_input('Quantidade de Notas Promissórias:', min_value = 1, max_value=120)
    data_primeiro_vencimento = col2.date_input("Data do 1º vencimento:", format="DD/MM/YYYY")
    valor_parcela = col1.number_input('Valor da parcela:')
    valor_total = f'{quantidade_notas * valor_parcela:_.2f}'.replace('.',',').replace('_','.')
    col1.write(f'O valor total será de **R$ {valor_total}**')
    cidade_estado = col2.text_input('Pagável em (Cidade/UF):', max_chars=100)
    st.divider()

    # Dados do credor
    st.subheader('Dados do Credor', anchor=False)
    col3, col4 = st.columns([1, 1])
    nome_credor = col3.text_input('Nome do Credor:', max_chars=40)
    cpf_cnpj_credor = col4.text_input('CPF/CNPJ do Credor (somente números):', max_chars=14)
    st.divider()

    # Dados do devedor
    st.subheader('Dados do Devedor', anchor=False)
    col5, col6 = st.columns([1, 1])
    nome_devedor = col5.text_input('Nome do Devedor:', max_chars=50)
    cpf_cnpj_devedor = col6.text_input('CPF/CNPJ do Devedor (somente números):', max_chars=14)
    endereco_devedor = st.text_input('Endereço completo do Devedor:', max_chars=85)
    st.divider()

    # Dados do 1º avalista
    st.subheader('Dados do 1º Avalista (opcional)', anchor=False)
    st.warning('Não é obrigatório possuir avalista para emitir nota promissória')
    col7, col8 = st.columns([1, 1])
    nome_avalista_1 = col7.text_input('Nome do 1º Avalista:', max_chars=32)
    cpf_cnpj_avalista_1 = col8.text_input('CPF/CNPJ do 1º Avalista (somente números):', max_chars=14)
    st.divider()

    # Dados do 2º avalista
    st.subheader('Dados do 2º Avalista (opcional)', anchor=False)
    col9, col10 = st.columns([1, 1])
    nome_avalista_2 = col9.text_input('Nome do 2º Avalista:', max_chars=32)
    cpf_cnpj_avalista_2 = col10.text_input('CPF/CNPJ do 2º Avalista (somente números):', max_chars=14)

    # Criar JSON
    def criar_json(
            quantidade_notas,
            data_primeiro_vencimento,
            cidade_estado,
            valor_parcela,
            nome_credor,
            cpf_cnpj_credor,
            nome_devedor,
            cpf_cnpj_devedor,
            endereco_devedor,
            nome_avalista_1,
            cpf_cnpj_avalista_1,
            nome_avalista_2,
            cpf_cnpj_avalista_2
    ):

        dados = {
            "quantidade_notas":quantidade_notas,
            "data_primeiro_vencimento":data_primeiro_vencimento,
            "cidade_estado":cidade_estado,
            "valor_parcela":valor_parcela,
            "nome_credor":nome_credor,
            "cpf_cnpj_credor":cpf_cnpj_credor,
            "nome_devedor":nome_devedor,
            "cpf_cnpj_devedor":cpf_cnpj_devedor,
            "endereco_devedor":endereco_devedor,
            "nome_avalista_1":nome_avalista_1,
            "cpf_cnpj_avalista_1":cpf_cnpj_avalista_1,
            "nome_avalista_2":nome_avalista_2,
            "cpf_cnpj_avalista_2":cpf_cnpj_avalista_2,
            }

        with open("dados.json","w") as arq_json:
            json.dump(dados, arq_json, default=str)
    
    def deletar_pdf(nome="./pdf_nota_promissoria.pdf"):
        if os.path.exists(nome):
            os.remove(nome)
    
    def criar_pdf():
        criar_json(
            quantidade_notas=quantidade_notas,
            data_primeiro_vencimento=data_primeiro_vencimento,
            cidade_estado=cidade_estado,
            valor_parcela=valor_parcela,
            nome_credor=nome_credor,
            cpf_cnpj_credor=cpf_cnpj_credor,
            nome_devedor=nome_devedor,
            cpf_cnpj_devedor=cpf_cnpj_devedor,
            endereco_devedor=endereco_devedor,
            nome_avalista_1=nome_avalista_1,
            cpf_cnpj_avalista_1=cpf_cnpj_avalista_1,
            nome_avalista_2=nome_avalista_2,
            cpf_cnpj_avalista_2=cpf_cnpj_avalista_2,
        )
        subprocess.run(["python3", "export_pdf.py"])

        with open("pdf_nota_promissoria.pdf", "rb") as pdf:
            pdf_bytes = pdf.read()
        return io.BytesIO(pdf_bytes)
    
    st.divider()

    # Botão download
    col11, col12, col13 = st.columns([1, 1, 1])
    botao_download = col11.download_button("Emitir em PDF", criar_pdf(), "nota_promissoria.pdf", "application/pdf", on_click=deletar_pdf(), use_container_width=True)




#########################################################################
################### PÁGINA NOTA PROMISSÓRIA EM BRANCO ###################
#########################################################################

if selected == 'Nota Promissória em branco':
    
    # Dados na nota promissória
    st.subheader('Emitir nota promissória em branco')
    col1, col2 = st.columns([1, 1])
    quantidade_notas = col1.number_input('Quantidade de Notas Promissórias:', min_value = 1)
    botao_nota_em_branco = col1.button('Emitir em PDF', use_container_width=True)
    #st.divider()



#########################################################################
################# PÁGINA O QUE É UMA NOTA PROMISSÓRIA? ##################
#########################################################################

if selected == 'O que é Nota Promissória?':
    st.subheader('O que é uma Nota Promissória? :pencil:')
    st.markdown('A nota promissória é um documento que **formaliza a existência de uma dívida**, em que seu devedor assume a obrigação de pagar ao credor o valor expresso no título. ' 
                'Também é um **título executivo**, ou seja, caso não seja paga, o credor pode dar início a uma ação de execução para cobrar a dívida.')
    st.image('nota_promissoria.png')
    st.caption('Esse é o modelo de nota promissória gerado através deste _site_. :sunglasses:')
    st.markdown('Uma **ação de execução** é uma forma mais rápida de cobrar o devedor, pois não se discute se existe a dívida ou não. Simplesmente, se cobra o devedor '
                'penhorando seus bens e valores em conta bancária. Bem diferente da ação de cobrança, onde o credor precisará provar a existência da dívida.')
    st.markdown('Portanto, quando for fazer negócios, utilize a nota promissória para maior garantia de recebimento!')
    st.subheader('O que é um avalista?')
    st.markdown('Um avalista é um terceiro que oferece o seu **aval** de que a dívida será paga. Ou seja, o avalista oferece a sua garantia pessoal de que se o devedor '
                'não pagar a dívida, ele pagará. Caso o devedor não pague a dívida, o avalista deverá ser acionado e pode responder judicialmente junto com o devedor, caso a dívida não seja paga.')



#########################################################################
######################### PÁGINA TERMOS DE USO ##########################
#########################################################################

if selected == 'Termos de uso':
    st.subheader(f'Termos de Uso :pencil:') 
    st.markdown('Ao utilizar o site *www.emitirnotapromissoria.com.br* o usuário declara ter ciência de que não iremos partilhar ou distrubuir as informações que você nos confiou, pois o mesmo não armazena os dados utilizados para gerar as notas promissórias.')
    st.markdown('Este site foi criado com o intuito de ajudá-lo a automatizar suas notas promissórias. A nota promissória é um documento válido judicialmente, saiba que ao utilizar este recurso, você será totalmente responsável pelas informações prestadas. Nos isentamos de eventuais inconsistências de informações fornecidas durante o preenchimento e sua total responsabilidade de você conferir as notas apos elas serem geradas!')







