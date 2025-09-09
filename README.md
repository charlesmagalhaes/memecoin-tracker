# Memecoin Tracker / Stock Tracker

Sistema backend para rastrear preços de memecoins ou ações, salvar histórico no Google Sheets e enviar alertas no Telegram. Funciona 24h/dia usando **GitHub Actions**.

---

## 🚀 Funcionalidades

- Buscar preços e variação percentual de memecoins (CoinGecko) ou ações (Yahoo Finance).  
- Salvar histórico automaticamente no Google Sheets.  
- Enviar alertas no Telegram quando houver variação acima do limite configurado.  
- Visualização de histórico e gráficos no Python/Colab.  
- Roda automaticamente em intervalos regulares via GitHub Actions.

---

## 📦 Tecnologias utilizadas

- Python 3.10+  
- gspread / oauth2client (Google Sheets)  
- requests (requisições HTTP)  
- pandas (manipulação de dados)  
- matplotlib (visualização de dados)  
- yfinance (opcional, para ações)  
- GitHub Actions (automação 24h)  
- Telegram Bot API (alertas)

---

## ⚙️ Configuração

### 1. Google Sheets

1. Crie uma planilha chamada `Memecoin Tracker`.  
2. Adicione os cabeçalhos na primeira linha:  
3. Crie uma **Service Account** no [Google Cloud](https://console.cloud.google.com/) e baixe o `credentials.json`.  
4. Compartilhe a planilha com o e-mail da service account como **Editor**.

---

### 2. Telegram

1. Crie um bot via **@BotFather** no Telegram.  
2. Salve o **bot_token** fornecido.  
3. Envie uma mensagem para o bot e use a API `getUpdates` para descobrir seu **chat_id**.

---

### 3. GitHub

1. Crie um repositório no GitHub e envie o código.  
2. Vá em **Settings → Secrets and Variables → Actions → New repository secret** e adicione:  
- `GOOGLE_CREDENTIALS` → conteúdo do `credentials.json`  
- `TELEGRAM_TOKEN` → token do bot  
- `TELEGRAM_CHAT_ID` → seu chat ID

---

## 💻 Estrutura do projeto


---

## ⏱ GitHub Actions

- Rodará automaticamente a cada 15 minutos (ou intervalo configurado no `cron`).  
- Workflow: `.github/workflows/tracker.yml`  

Exemplo do cron:

```yaml
schedule:
  - cron: "*/15 * * * *"  # a cada 15 minutos
📈 Uso

Clone o repositório:

git clone https://github.com/seu-usuario/memecoin-tracker.git


Instale dependências:

pip install -r requirements.txt


Configure secrets no GitHub Actions (Google + Telegram).

Commit e push → o GitHub Actions roda automaticamente.
