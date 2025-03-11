!pip install google-play-scraper
from google_play_scraper import reviews, Sort
import pandas as pd
from google.colab import files

# ID do app na Play Store
app_id = "br.com.phaneronsoft.rotinadivertida"

# Coletar 500 comentários com mais informações
comentarios, _ = reviews(
    app_id,
    lang="pt",  
    country="br",  
    count=500, 
    sort=Sort.NEWEST  
)

# Converter para DataFrame e incluir mais colunas
df = pd.DataFrame(comentarios)[["userName", "score", "content", "thumbsUpCount", "at", "replyContent", "reviewId"]]

# Salvar como CSV
arquivo_csv = "feedbacks_playstore.csv"
df.to_csv(arquivo_csv, index=False)

# Baixar o arquivo no Google Colab
files.download(arquivo_csv)

df.head()