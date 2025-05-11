
import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- CONFIGURAZIONI ---
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
AMAZON_TRACKING_ID = st.secrets["AMAZON_TRACKING_ID"]

st.title("📸 Trova Prezzo da Immagine")

uploaded_file = st.file_uploader("Carica una foto dell'articolo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Immagine caricata", use_column_width=True)

    with st.spinner("Sto analizzando l'immagine con l'AI..."):

        # Converti immagine in base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode()

        # Carica l'immagine su un server temporaneo (imgur non disponibile: usiamo file.io o simili)
        upload_response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": "8f71f1d857c9e71a7e77fe1e74a8d689"},
            files={"image": img_bytes}
        )

        if upload_response.status_code == 200:
            image_url = upload_response.json()["data"]["url"]

            # Invia l'immagine al modello BLIP su Replicate
            headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
            payload = {
                "version": "fb9f9de1c6169c3f02e85c709c7067fa72c7d96f291cf1fa9794c07c6a9b26d4",
                "input": {"image": image_url}
            }

            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                json=payload,
                headers=headers
            )

            if response.status_code == 201:
                prediction_url = response.json()["urls"]["get"]

                # Aspetta la risposta definitiva
                import time
                status = "starting"
                while status not in ["succeeded", "failed"]:
                    prediction_status = requests.get(prediction_url, headers=headers).json()
                    status = prediction_status["status"]
                    time.sleep(1)

                if status == "succeeded":
                    descrizione = prediction_status["output"]
                    st.success(f"🧠 L'AI ha riconosciuto: **{descrizione}**")

                    # Crea il link affiliato Amazon
                    descrizione_clean = descrizione.replace(" ", "+")
                    amazon_url = f"https://www.amazon.it/s?k={descrizione_clean}&tag={AMAZON_TRACKING_ID}"
                    st.markdown(f"🔗 [Vedi offerte su Amazon]({amazon_url})")
                else:
                    st.error("Errore nel riconoscimento AI.")
            else:
                st.error("Errore nella chiamata a Replicate.")
        else:
            st.error("Errore nel caricamento dell'immagine (imgBB).")
