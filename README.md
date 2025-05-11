# 📸 Trova Prezzi da Immagine

Trova l'offerta migliore partendo da una semplice foto!  
Questa web app usa l'intelligenza artificiale per riconoscere un prodotto da un'immagine e cerca subito il miglior prezzo su Amazon (con link affiliato).

## 🚀 Funzionalità

- Carica una foto del prodotto
- L'AI lo riconosce automaticamente (con modello BLIP)
- Ti propone il miglior affare su Amazon
- Link affiliato per guadagno passivo

## 🔧 Tecnologia usata

- Python & Streamlit
- Replicate API (modello BLIP per riconoscimento immagini)
- Amazon Affiliate Program
- Hosting gratuito su [Streamlit Cloud](https://streamlit.io/cloud)

## 🧠 Come usarla

1. Carica una foto di un oggetto
2. L'AI ne descrive il contenuto
3. Clicca sul link per vedere i migliori prezzi

## 📦 Esempio online

🔗 [Apri l'app Web (Streamlit)](https://TUA-URL.streamlit.app) ← *(aggiorna con il tuo link dopo il deploy)*

## 🔐 Configurazione (secrets)

Nella cartella `.streamlit/` inserisci il file `secrets.toml` con i tuoi dati:

```toml
REPLICATE_API_TOKEN = "la-tua-replicate-api"
AMAZON_TRACKING_ID = "iltuonome-21"
