import streamlit as st
import tempfile
import os
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# === CONFIGURATION DE LA PAGE ===
st.set_page_config(page_title="Agent PDF Qwen", layout="wide")
st.title("🤖 Agent PDF avec Qwen")
st.caption("Upload un PDF, pose ta question, obtiens une réponse (100% local et confidentiel).")

# === CONFIGURATION DES MODÈLES ===
MODEL_NAME = "qwen3.8:27b"
EMBED_MODEL_NAME = "nomic-embed-text"


@st.cache_resource
def get_models():
    # SOLUTION DU TIMEOUT : request_timeout=300.0 donne 5 minutes au modèle pour répondre
    llm = Ollama(model=MODEL_NAME, request_timeout=300.0)
    embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME)
    return llm, embed_model


llm, embed_model = get_models()
Settings.llm = llm
Settings.embed_model = embed_model

# === ZONE D'UPLOAD DU PDF ===
uploaded_file = st.file_uploader("📎 Clique ici pour choisir un fichier PDF à analyser", type=["pdf"])

if uploaded_file is not None:
    # Créer un dossier temporaire pour que LlamaIndex puisse lire le fichier
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Clé unique pour l'historique de chat basé sur le nom du fichier
    chat_key = f"messages_{uploaded_file.name}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        st.session_state[f"engine_{uploaded_file.name}"] = None

    # Si l'index n'est pas encore créé pour ce fichier, on le crée
    if st.session_state[f"engine_{uploaded_file.name}"] is None:
        with st.spinner("📖 Lecture et analyse du PDF en cours... (cela peut prendre 1 à 2 minutes)"):
            try:
                documents = SimpleDirectoryReader(temp_dir).load_data()
                index = VectorStoreIndex.from_documents(documents)
                st.session_state[f"engine_{uploaded_file.name}"] = index.as_query_engine()
                st.success(f"✅ '{uploaded_file.name}' est prêt ! Pose ta question ci-dessous.")
            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")

            # Nettoyage du fichier temporaire après l'indexation
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

    # === INTERFACE DE CHAT ===
    query_engine = st.session_state[f"engine_{uploaded_file.name}"]

    if query_engine is not None:
        # Affichage de l'historique
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Zone de saisie de la question
        if question := st.chat_input("Pose ta question sur ce PDF..."):
            # Message de l'utilisateur
            st.session_state[chat_key].append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            # Réponse de l'IA
            with st.chat_message("assistant"):
                with st.spinner("🤔 L'IA réfléchit et cherche dans le document..."):
                    try:
                        response = query_engine.query(question)
                        reponse_texte = str(response)
                        st.markdown(reponse_texte)
                    except Exception as e:
                        st.error(f"Erreur de réponse : {e}")

            st.session_state[chat_key].append({"role": "assistant", "content": reponse_texte})
else:
    st.info("👈 Commence par uploader un fichier PDF ci-dessus pour démarrer l'analyse.")
