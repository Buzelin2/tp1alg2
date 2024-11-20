import streamlit as st

# Configuração inicial da página
st.set_page_config(page_title="Meu Trabalho de Algoritmos 2", layout="centered")

# Título principal
st.title("TP1 de Algoritmos 2 (Arthur Buzelin e Caio Santana)")

# Descrição opcional
st.write("Este é um trabalho de Algoritmos 2, feito por Arthur Buzelin Galery e Caio Santana Trigueiro. \
    Neste trabalho ele é organizado em 3 pastas diferentes: 'original', 'decompressed' e 'compressed'. O código \
        consegue ser rodado para comprimir ou descomprimir um arquivo, de diferentes extensões, neste trabalho foram testados txt, bmp e pdf. \
            Com isso, o código também pode ser rodado para diferentes quantidades de bits. Por padrão e ao passar o argumento f (falso para bits váriaveis) \
                o código irá comprimir o arquivo com 12 bits. Caso seja passado o argumento t (verdadeiro para bits variáveis) o código irá comprimir o arquivo com a quantidade especificada de bits.\
                    Para cada um dos 3 tipos de arquivo, iremos mostrar o plot de linha variando a quantidade de bits, um bar graph com o peso da melhor compressão em comparação com o original e também uma opção para ver o tempo de rodar")


st.write("Bem agora, partindo para uma análise, a primeira coisa que fizemos foi analisar um arquivo txt, escolhemos o enunciado do trabalho. \
    Como funciona? Bem nós utilizamos o código para comprimir, definindo os parametros na hora, ele irá ficar salvo na pasta compressed e ao utilizar o comando no código de descompressão \
        ele será descomprimido, retornando perfeitamente ao arquivo original, na pasta decompressed.")

st.write("Com isso conseguimos agora fazer algumas análises mais interessantes. Primeiro geramos um gráfico para saber para este arquivo qual seria a quantidade perfeita de bits para a compressão/descompressão. \
O gráfico pode ser visto logo abaixo. Como podemos ver ele sobe muito rápido e estabiliza em uma taxa de compressão quase 2 vezes melhor do que o tamanho original.")
# Rodapé



import streamlit as st
import matplotlib.pyplot as plt

# Dados fornecidos
bits_utilizados = [9, 10, 11, 12, 13, 14, 15, 16]
taxas_compressao = [1.45, 1.76, 1.86, 1.91, 1.91, 1.91, 1.91, 1.91]

# Título e descrição
st.subheader("Taxa de Compressão por Quantidade de Bits")

# Criando o gráfico
fig, ax = plt.subplots()
ax.plot(bits_utilizados, taxas_compressao, marker="o", linestyle="-")
ax.set_title("Taxa de Compressão por Bits Utilizados")
ax.set_xlabel("Bits Utilizados")
ax.set_ylabel("Taxa de Compressão")
ax.grid(True)

# Exibindo o gráfico no Streamlit
st.pyplot(fig)

import streamlit as st
import matplotlib.pyplot as plt

# Dados fornecidos
nomes_txt = ["Antes da Compressão", "Depois da Compressão"]
tamanhos_txt = [9281, 4850]  # Tamanhos em bytes

# Título da seção
st.subheader("Tamanhos do Arquivo TXT Antes e Depois da Compressão")

# Criando o gráfico de barras
fig_txt, ax_txt = plt.subplots()
ax_txt.bar(nomes_txt, tamanhos_txt, color=["blue", "green"])
ax_txt.set_title("Comparação de Tamanho: TXT Antes x Depois da Compressão")
ax_txt.set_ylabel("Tamanho (bytes)")
ax_txt.set_xlabel("Estado do Arquivo")
ax_txt.bar_label(ax_txt.containers[0], fmt="%.0f bytes")  # Adiciona os valores em cima das barras
ax_txt.grid(axis='y', linestyle="--", alpha=0.7)

# Exibindo o gráfico no Streamlit
st.pyplot(fig_txt)

# Informações adicionais
st.write("Este gráfico compara o tamanho do arquivo TXT antes e depois da compressão.")
st.write(f"Tamanho Antes da Compressão: **{tamanhos_txt[0]:,} bytes**")
st.write(f"Tamanho Depois da Compressão: **{tamanhos_txt[1]:,} bytes**")


bits_utilizados_txt = [9, 10, 11, 12, 13, 14, 15, 16]
tempos_execucao_txt = [0.04, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]

# Dados do arquivo pdf
bits_utilizados_pdf = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
tempos_execucao_pdf = [16.33, 18.53, 17.76, 21.73, 21.75, 18.19, 16.06, 14.37, 14.16, 13.10]


if st.checkbox("Exibir gráfico de Tempo de Execução para o arquivo txt"):
    fig_time_txt, ax_time_txt = plt.subplots()
    ax_time_txt.plot(bits_utilizados_txt, tempos_execucao_txt, marker="o", linestyle="--", color="blue", label="Tempo de Execução (txt)")
    ax_time_txt.set_title("Tempo de Execução por Bits Utilizados (txt)")
    ax_time_txt.set_xlabel("Bits Utilizados")
    ax_time_txt.set_ylabel("Tempo de Execução (segundos)")
    ax_time_txt.grid(True)
    ax_time_txt.legend()
    st.pyplot(fig_time_txt)



st.write("Agora vamos analisar uma imagem para testar o nosso algoritmo de compressão e descompressão. Resolvemos utilizar a seguinte imagem de gatinho:")



import streamlit as st
from PIL import Image

# Título da seção
st.subheader("Visualização da Imagem Original: gato.bmp")

# Carregando e exibindo a imagem
try:
    # Substitua pelo caminho correto se a imagem não estiver no mesmo diretório
    image_path = "gato.bmp"  
    image = Image.open(image_path)
    st.image(image, caption="Imagem Original: gato.bmp", width = 300)
except FileNotFoundError:
    st.error("Erro: O arquivo gato.bmp não foi encontrado. Verifique o caminho.")

# Informações adicionais
st.write("Com essa imagem fizemos os mesmos testes anteriores, variando a quantidade de bits. Essa por ser uma imagem muito simples, com poucos detalhes, ou seja sendo facilmente comprimivel, o algoritmo teve resultados excelentes! Melhorando quase 20 vezes!")




import streamlit as st
import matplotlib.pyplot as plt

# Dados fornecidos
bits_utilizados = [9, 10, 11, 12, 13, 14, 15, 16]
taxas_compressao = [1.55, 1.70, 9.92, 17.50, 19.28, 19.36, 19.36, 19.36]
tempos_execucao = [11.52, 8.05, 1.60, 1.61, 1.83, 2.07, 2.05, 2.19]

# Título da seção
st.subheader("Taxa de Compressão por Quantidade de Bits - Arquivo gato.bmp")

# Gráfico de linha da taxa de compressão
fig, ax = plt.subplots()
ax.plot(bits_utilizados, taxas_compressao, marker="o", linestyle="-", label="Taxa de Compressão")
ax.set_title("Taxa de Compressão por Bits Utilizados")
ax.set_xlabel("Bits Utilizados")
ax.set_ylabel("Taxa de Compressão")
ax.grid(True)
ax.legend()



# Exibindo o gráfico no Streamlit
st.pyplot(fig)

import streamlit as st
import matplotlib.pyplot as plt

# Dados fornecidos
nomes = ["Não Comprimido", "Comprimido"]
tamanhos = [262282, 13547]  # Tamanhos em bytes

# Título da seção
st.subheader("Tamanhos do Arquivo gato.bmp")

# Criando o gráfico de barras
fig, ax = plt.subplots()
ax.bar(nomes, tamanhos, color=["blue", "green"])
ax.set_title("Comparação de Tamanho: Arquivo Comprimido x Não Comprimido")
ax.set_ylabel("Tamanho (bytes)")
ax.set_xlabel("Estado do Arquivo")
ax.bar_label(ax.containers[0], fmt="%.0f bytes")  # Adiciona os valores em cima das barras
ax.grid(axis='y', linestyle="--", alpha=0.7)

# Exibindo o gráfico no Streamlit
st.pyplot(fig)

# Informações adicionais


# Informações adicionais
st.write("Este gráfico mostra a relação entre a taxa de compressão e o número de bits utilizados para o arquivo gato.bmp.")

# Gráfico opcional: tempo de execução por bits utilizados
if st.checkbox("Exibir gráfico de Tempo de Execução por Bits Utilizados"):
    fig_time, ax_time = plt.subplots()
    ax_time.plot(bits_utilizados, tempos_execucao, marker="o", linestyle="--", color="orange", label="Tempo de Execução")
    ax_time.set_title("Tempo de Execução por Bits Utilizados")
    ax_time.set_xlabel("Bits Utilizados")
    ax_time.set_ylabel("Tempo de Execução (segundos)")
    ax_time.grid(True)
    ax_time.legend()
    st.pyplot(fig_time)
# Informações adicionais


import streamlit as st
import matplotlib.pyplot as plt

# Dados fornecidos
bits_utilizados = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
taxas_compressao = [0.92, 0.83, 0.77, 0.72, 0.71, 0.72, 0.76, 0.80, 0.85, 0.85]
tempos_execucao = [16.33, 18.53, 17.76, 21.73, 21.75, 18.19, 16.06, 14.37, 14.16, 13.10]

# Título da seção

st.write("Agora, utilizamos o pdf do enunciado do tp para tentar comprimi-lo. Como pode-se ver abaixo para o tipo pdf acabamos não tendo um resultado tão legal quanto os outros, porém isso pode acabar indicando determinadas limitações no algoritmo, mas, sabemos que ao trasnformar para texto a compressão funciona muito bem para o enunciado, dessa forma, uma abordagem de trasnformar para texto primeiro resolveria o problema.")
st.subheader("Gráficos para o Arquivo tp1.pdf")

# Gráfico 1: Taxa de Compressão por Bits Utilizados
fig1, ax1 = plt.subplots()
ax1.plot(bits_utilizados, taxas_compressao, marker="o", linestyle="-", label="Taxa de Compressão")
ax1.set_title("Taxa de Compressão por Bits Utilizados")
ax1.set_xlabel("Bits Utilizados")
ax1.set_ylabel("Taxa de Compressão")
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)

import streamlit as st
import matplotlib.pyplot as plt

# Dados fornecidos
nomes_pdf = ["Antes da Compressão", "Depois da Compressão"]
tamanhos_pdf = [204400, 223007]  # Tamanhos em bytes

# Título da seção
st.subheader("Tamanhos do Arquivo PDF Antes e Depois da Compressão")

# Criando o gráfico de barras
fig_pdf, ax_pdf = plt.subplots()
ax_pdf.bar(nomes_pdf, tamanhos_pdf, color=["blue", "red"])
ax_pdf.set_title("Comparação de Tamanho: PDF Antes x Depois da Compressão")
ax_pdf.set_ylabel("Tamanho (bytes)")
ax_pdf.set_xlabel("Estado do Arquivo")
ax_pdf.bar_label(ax_pdf.containers[0], fmt="%.0f bytes")  # Adiciona os valores em cima das barras
ax_pdf.grid(axis='y', linestyle="--", alpha=0.7)

# Exibindo o gráfico no Streamlit
st.pyplot(fig_pdf)


if st.checkbox("Exibir gráfico de Tempo de Execução para o arquivo pdf"):
    fig_time_pdf, ax_time_pdf = plt.subplots()
    ax_time_pdf.plot(bits_utilizados_pdf, tempos_execucao_pdf, marker="o", linestyle="--", color="orange", label="Tempo de Execução (pdf)")
    ax_time_pdf.set_title("Tempo de Execução por Bits Utilizados (pdf)")
    ax_time_pdf.set_xlabel("Bits Utilizados")
    ax_time_pdf.set_ylabel("Tempo de Execução (segundos)")
    ax_time_pdf.grid(True)
    ax_time_pdf.legend()
    st.pyplot(fig_time_pdf)

# Informações adicionais sobre o primeiro gráfico
st.write("### Conclusão")
st.write(
    "Através deste trabalho, foi possível explorar as capacidades do algoritmo de compressão LZW para diferentes tipos de arquivos, "
    "como textos, imagens e PDFs. Cada tipo de arquivo apresentou diferentes comportamentos em relação à taxa de compressão e ao tempo de execução:\n"
    "\n- **Arquivos TXT**: Apresentaram excelente compressibilidade, com taxas de compressão que melhoraram em quase o dobro em relação ao espaço armazenado. "
    "Isso destaca a eficiência do LZW para arquivos de texto.\n"
    "\n- **Imagens (BMP)**: Com a baixa complexidade da imagem exemplo, o arquivo BMP comprimido demonstrou resultados "
    "impressionantes, atingindo compressões quase 20 vezes menores que o tamanho original.\n"
    "\n- **Arquivos PDF**: O algoritmo apresentou limitações, como aumento do tamanho do arquivo após a compressão. Isso ocorre devido à estrutura complexa "
    "e ao alto nível de entropia dos PDFs. Contudo, ao transformar o PDF para texto puro antes da compressão, seria possível melhorar os resultados."
)