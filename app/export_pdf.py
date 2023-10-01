# Importa a biblioteca que manipula PDFs
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

#Importa a biblioteca qiue manipula datas
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Importa a biblioteca que converte números em números por extenso
from num2words import num2words

# Importa a biblioteca que trata separador de milhar e vírgulas
import locale

# Impoeta a biblioteca JSON
import json



# Defina a localização para o formato monetário brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Cria um PDF em branco
cnv = canvas.Canvas('pdf_nota_promissoria.pdf', pagesize=A4)

# Carrega a imagem
img = 'nota_promissoria.png'

# Abre o arquivo JSON
def abrir_json():
    with open('dados.json', "r") as arq_json:
        return json.load(arq_json)
    
dados = abrir_json()


# Define todas as variáveis usando o arquivo JSON
quantidade_notas = dados["quantidade_notas"]
data_vencimento = dados["data_primeiro_vencimento"]
cidade_estado = dados["cidade_estado"].strip().title()
valor_parcela = dados["valor_parcela"]
valor_parcela_formatado = locale.currency(valor_parcela, grouping=True, symbol=False)

nome_credor = dados["nome_credor"].strip().title()
cpf_cnpj_credor = dados["cpf_cnpj_credor"].strip().replace('.',"").replace('-',"").replace('/',"").replace(' ',"")
nome_devedor = dados["nome_devedor"].strip().title()
cpf_cnpj_devedor = dados["cpf_cnpj_devedor"].strip().replace('.',"").replace('-',"").replace('/',"").replace(' ',"")
endereco_devedor = dados["endereco_devedor"].strip().title()

nome_avalista_1 = dados["nome_avalista_1"].strip().title()
cpf_cnpj_avalista_1 = dados["cpf_cnpj_avalista_1"].strip().replace('.',"").replace('-',"").replace('/',"").replace(' ',"")
nome_avalista_2 = dados["nome_avalista_2"].strip().title()
cpf_cnpj_avalista_2 = dados["cpf_cnpj_avalista_2"].strip().replace('.',"").replace('-',"").replace('/',"").replace(' ',"")


# Tratamento de CPF/CPNJ

# Credor
if len(cpf_cnpj_credor) == 11: # Identifica se é um CPF
    cpf_cnpj_credor = cpf_cnpj_credor[0:3] + '.' + cpf_cnpj_credor[3:6] + '.' + cpf_cnpj_credor[6:9] + '-' + cpf_cnpj_credor[9:]
elif len(cpf_cnpj_credor) == 14: # Identifica se é um CNPJ
    cpf_cnpj_credor = cpf_cnpj_credor[0:2] + '.' + cpf_cnpj_credor[2:5] + '.' + cpf_cnpj_credor[5:8] + '/' + cpf_cnpj_credor[8:12] + '-' + cpf_cnpj_credor[12:]

#Devedor
if len(cpf_cnpj_devedor) == 11: # Identifica se é um CPF
    cpf_cnpj_devedor = cpf_cnpj_devedor[0:3] + '.' + cpf_cnpj_devedor[3:6] + '.' + cpf_cnpj_devedor[6:9] + '-' + cpf_cnpj_devedor[9:]
elif len(cpf_cnpj_devedor) == 14: # Identifica se é um CNPJ
    cpf_cnpj_devedor = cpf_cnpj_devedor[0:2] + '.' + cpf_cnpj_devedor[2:5] + '.' + cpf_cnpj_devedor[5:8] + '/' + cpf_cnpj_devedor[8:12] + '-' + cpf_cnpj_devedor[12:]

# Avalista 1
if len(cpf_cnpj_avalista_1) == 11: # Identifica se é um CPF
    cpf_cnpj_avalista_1 = cpf_cnpj_avalista_1[0:3] + '.' + cpf_cnpj_avalista_1[3:6] + '.' + cpf_cnpj_avalista_1[6:9] + '-' + cpf_cnpj_avalista_1[9:]
elif len(cpf_cnpj_avalista_1) == 14: # Identifica se é um CNPJ
    cpf_cnpj_avalista_1 = cpf_cnpj_avalista_1[0:2] + '.' + cpf_cnpj_avalista_1[2:5] + '.' + cpf_cnpj_avalista_1[5:8] + '/' + cpf_cnpj_avalista_1[8:12] + '-' + cpf_cnpj_avalista_1[12:]

# Avalista 2
if len(cpf_cnpj_avalista_2) == 11: # Identifica se é um CPF
    cpf_cnpj_avalista_2 = cpf_cnpj_avalista_2[0:3] + '.' + cpf_cnpj_avalista_2[3:6] + '.' + cpf_cnpj_avalista_2[6:9] + '-' + cpf_cnpj_avalista_2[9:]
elif len(cpf_cnpj_avalista_2) == 14: # Identifica se é um CNPJ
    cpf_cnpj_avalista_2 = cpf_cnpj_avalista_2[0:2] + '.' + cpf_cnpj_avalista_2[2:5] + '.' + cpf_cnpj_avalista_2[5:8] + '/' + cpf_cnpj_avalista_2[8:12] + '-' + cpf_cnpj_avalista_2[12:]




# Manipulando datas
data_primeiro_vencimento = datetime.strptime(data_vencimento, '%Y-%m-%d')
dia = str(data_primeiro_vencimento.day)
mes = str(data_primeiro_vencimento.month)
ano = str(data_primeiro_vencimento.year)

# DATAS
lista_datas = []
lista_datas.append(data_primeiro_vencimento)
indice_mes = 1
for i in range(0, quantidade_notas):
    data_futura = data_primeiro_vencimento + relativedelta(months=indice_mes)
    indice_mes += 1
    lista_datas.append(data_futura)

valor_parcela_por_extenso = num2words(valor_parcela, lang='pt-br') + ' reais'


# Desenhando a imagem e as strings
contador = 1
indice_datas = 0
for c in range(0, quantidade_notas):
    cnv.drawImage(image=img, x=12, y=445, width=572, height=359.75)

    cnv.drawString(x=127, y=767, text=f'{contador}/{quantidade_notas}') # Número da Nota
    cnv.drawString(x=260, y=770, text=str(lista_datas[indice_datas].day)) # Dia de vencimento


    if lista_datas[indice_datas].month == 1: mes_por_extenso = 'Janeiro'
    elif lista_datas[indice_datas].month == 2: mes_por_extenso = 'Fevereiro'
    elif lista_datas[indice_datas].month == 3: mes_por_extenso = 'Março'
    elif lista_datas[indice_datas].month == 4: mes_por_extenso = 'Abril'
    elif lista_datas[indice_datas].month == 5: mes_por_extenso = 'Maio'
    elif lista_datas[indice_datas].month == 6: mes_por_extenso = 'Junho'
    elif lista_datas[indice_datas].month == 7: mes_por_extenso = 'Julho'
    elif lista_datas[indice_datas].month == 8: mes_por_extenso = 'Agosto'
    elif lista_datas[indice_datas].month == 9: mes_por_extenso = 'Setembro'
    elif lista_datas[indice_datas].month == 10: mes_por_extenso = 'Outubro'
    elif lista_datas[indice_datas].month == 11: mes_por_extenso = 'Novembro'
    elif lista_datas[indice_datas].month == 12: mes_por_extenso = 'Dezembro'


    cnv.drawString(x=307, y=770, text=mes_por_extenso) # Mês de vencimento
    cnv.drawString(x=400, y=770, text=str(lista_datas[indice_datas].year)) # Ano de vencimento
    cnv.drawString(x=495, y=766, text=valor_parcela_formatado) # Valor da parcela

    cnv.drawString(x=125, y=720, text=str(lista_datas[indice_datas].day) + ' de ' + mes_por_extenso + ' de ' + str(lista_datas[indice_datas].year)) # Data por extenso
    cnv.drawString(x=90, y=699, text=nome_credor) # Nome do credor
    cnv.drawString(x=420, y=699, text=cpf_cnpj_credor) # CPF/CNPJ do credor
    cnv.drawString(x=220, y=678, text=valor_parcela_por_extenso) # CPF/CNPJ do credor
    cnv.drawString(x=282, y=658, text=cidade_estado) # Local de pagamento

    cnv.drawString(x=133, y=619, text=nome_devedor) # Nome do devedor
    cnv.drawString(x=475, y=619, text=cpf_cnpj_devedor) # CPF/CNPJ do devedor
    cnv.drawString(x=135, y=597, text=endereco_devedor) # Endereço do devedor

    cnv.drawString(x=119, y=544, text=nome_avalista_1) # Nome do avalista 1
    cnv.drawString(x=140, y=530, text=cpf_cnpj_avalista_1) # CPF/CNPJ do devedor
    cnv.drawString(x=363, y=543, text=nome_avalista_2) # Nome do devedor
    cnv.drawString(x=383, y=530, text=cpf_cnpj_avalista_2) # CPF/CNPJ do devedor

    cnv.drawString(x=15, y=68, text='Nota promissória gerada via website.')
    cnv.drawString(x=15, y=50, text='Para checar a veracidade, acesse https://www.emitirnotapromissoria.com.br')
    cnv.showPage()

    contador += 1
    indice_datas +=1


# Salva o documento
cnv.save()








