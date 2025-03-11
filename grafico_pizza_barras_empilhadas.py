# Instalar bibliotecas necessárias
!pip install google-play-scraper pandas matplotlib

# Importar bibliotecas
from google_play_scraper import reviews
import pandas as pd
import matplotlib.pyplot as plt

# ID do app na Play Store
app_id = "br.com.phaneronsoft.rotinadivertida"

# Buscar os comentários
comentarios, _ = reviews(
    app_id,
    lang='pt',  
    country='br',  
    count=500  
)

# Criar um DataFrame
df = pd.DataFrame(comentarios)

# Converter a data
df['at'] = pd.to_datetime(df['at'])

# Criar coluna de Ano e Bimestre com formato legível
bimestres = {
    "01": "Jan-Fev", "02": "Jan-Fev",
    "03": "Mar-Abr", "04": "Mar-Abr",
    "05": "Mai-Jun", "06": "Mai-Jun",
    "07": "Jul-Ago", "08": "Jul-Ago",
    "09": "Set-Out", "10": "Set-Out",
    "11": "Nov-Dez", "12": "Nov-Dez"
}

df['Ano'] = df['at'].dt.year
df['Mes'] = df['at'].dt.strftime('%m')  # Extrair o mês como string
df['Bimestre'] = df['Mes'].map(bimestres)  # Mapear para nomes legíveis
df['Periodo'] = df['Bimestre'] + " " + df['Ano'].astype(str) 

# Criar categorias para os comentários
def classificar_comentario(nota):
    if nota >= 4:
        return 'Bom'
    elif nota == 3:
        return 'Precisa Melhorar'
    else:
        return 'Ruim'

df['Classificacao'] = df['score'].apply(classificar_comentario)

# Calcular percentual geral
percentual_geral = df['Classificacao'].value_counts(normalize=True) * 100

# Criar gráfico de pizza geral
plt.figure(figsize=(6, 6))
percentual_geral.plot.pie(autopct='%1.1f%%', colors=['blue', 'orange', 'gray'])
plt.title("Distribuição de Comentários - Rotina Divertida")
plt.ylabel('')
plt.show()

# Criar DataFrame com percentuais por bimestre
percentual_bimestre = df.groupby(['Periodo', 'Classificacao']).size().unstack(fill_value=0)

# Converter para percentual por período
percentual_bimestre = percentual_bimestre.div(percentual_bimestre.sum(axis=1), axis=0) * 100

# Criar gráfico de barras empilhadas por bimestre
percentual_bimestre.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis')

plt.title("Evolução das Avaliações - Rotina Divertida")
plt.ylabel("Percentual (%)")
plt.xlabel("Ano e Bimestre")
plt.legend(title="Classificação")
plt.xticks(rotation=45, ha='right') 
plt.show()

# Salvar os dados processados para o Power BI
df.to_csv("comentarios_rotina_divertida.csv", index=False)

print("Arquivo salvo como 'comentarios_rotina_divertida.csv'")
