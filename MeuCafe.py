import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, filedialog, messagebox
from fpdf import FPDF
import os
import re

def limpar_nome_arquivo(nome):
    # Remove caracteres inválidos do nome do arquivo
    return re.sub(r'[<>:"/\\|?*]', '_', nome)

# Função para processar o arquivo CSV
def processar_csv(file_path):
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')

        # Mostra as colunas disponíveis
        colunas = df.columns.tolist()
        print(f"Colunas disponíveis: {colunas}")
        messagebox.showinfo("Colunas Disponíveis", f"Colunas disponíveis: {colunas}")

        # Colunas de interesse (algumas são categóricas)
        colunas_interesse = [
            "Qual a sua frequência de café diário?",
            "Seu café é com açúcar?",
            "Seu café é com leite?",
            "Qual o momento em que você mais toma café?"
        ]

        # Verifica se todas as colunas existem
        for coluna in colunas_interesse:
            if coluna not in df.columns:
                messagebox.showerror("Erro", f"A coluna '{coluna}' não foi encontrada.")
                return

        # Calcula moda, média e mediana
        resultados = {}
        
        for coluna in colunas_interesse:
            print(f"\nAnalisando a coluna: {coluna}")
            resultados[coluna] = {}

            # Cálculo da moda
            moda = df[coluna].mode()[0]
            resultados[coluna]['Moda'] = moda

            # Se a coluna for numérica, calcular média e mediana
            if df[coluna].dtype in ['int64', 'float64']:
                media = df[coluna].mean()
                mediana = df[coluna].median()
                resultados[coluna]['Média'] = media
                resultados[coluna]['Mediana'] = mediana
            else:
                resultados[coluna]['Média'] = "N/A"
                resultados[coluna]['Mediana'] = "N/A"

            print(f"Moda: {resultados[coluna]['Moda']}, Média: {resultados[coluna]['Média']}, Mediana: {resultados[coluna]['Mediana']}")

            # Gera gráfico de barras para cada coluna de interesse
            plt.figure(figsize=(10, 6))
            frequencia = df[coluna].value_counts()
            frequencia.plot(kind='bar', color='skyblue')
            plt.title(f'Frequência de: {coluna}')
            plt.xlabel(coluna)
            plt.ylabel('Frequência')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Salva o gráfico como uma imagem, utilizando função de limpeza
            imagem_gráfico = f"grafico_{limpar_nome_arquivo(coluna)}.png"
            print(f"Salvando gráfico como: {imagem_gráfico}")  # Debug
            plt.savefig(imagem_gráfico)
            plt.close()

            # Adiciona o gráfico ao dicionário de resultados
            resultados[coluna]['Imagem'] = imagem_gráfico

        # Cria um PDF para salvar os resultados
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Adiciona os resultados ao PDF
        for coluna, stats in resultados.items():
            pdf.cell(0, 10, f'Analisando a coluna: {coluna}', ln=True)
            pdf.cell(0, 10, f'Moda: {stats["Moda"]}', ln=True)
            pdf.cell(0, 10, f'Média: {stats["Média"]}', ln=True)
            pdf.cell(0, 10, f'Mediana: {stats["Mediana"]}', ln=True)
            pdf.cell(0, 10, '', ln=True)  # Linha em branco
            
            # Adiciona a imagem do gráfico ao PDF
            try:
                pdf.image(stats['Imagem'], x=10, w=180)  # x e largura podem ser ajustados
            except Exception as e:
                messagebox.showerror("Erro ao adicionar imagem", str(e))
            
            # Linha em branco após a imagem
            pdf.cell(0, 10, '', ln=True)

            # Remove a imagem temporária
            try:
                os.remove(stats['Imagem'])
            except Exception as e:
                print(f"Erro ao remover imagem: {e}")

        # Diálogo para salvar o PDF
        save_path = filedialog.asksaveasfilename(title="Salvar PDF", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_path:
            pdf.output(save_path)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em: {save_path}")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Função para abrir o diálogo de seleção de arquivos
def abrir_arquivo():
    file_path = filedialog.askopenfilename(title="Selecione um arquivo CSV", filetypes=[("CSV files", "*.csv")])
    if file_path:
        processar_csv(file_path)

# Configuração da interface gráfica
root = Tk()
root.title("Análise de Dados de Café")

# Adicionando um botão
botao = Button(root, text="Selecionar Arquivo CSV", command=abrir_arquivo, padx=10, pady=5)
botao.pack(pady=20)

# Adicionando um rótulo para indicar instruções
instrucoes_label = Label(root, text="Clique no botão acima para selecionar um arquivo CSV.")
instrucoes_label.pack(pady=10)

# Inicia o loop da interface gráfica
root.mainloop()