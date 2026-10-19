import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# === CONFIGURATION ===
MODEL_NAME = "qwen3.8:27b"
EMBED_MODEL_NAME = "nomic-embed-text"  # Modèle spécialisé pour les embeddings
PDF_FOLDER = "./documents"

# === TITRE DE L'APP ===
st.set_page_config(page_title="Agent PDF Qwen", layout="wide")
st.title(" Agent PDF avec Qwen")
st.caption("Analyse tes documents localement avec Qwen + LlamaIndex")


# === CHARGEMENT DES DOCUMENTS ===
@st.cache_resource
def charger_documents():
    print("📂 Chargement des documents...")
    documents = SimpleDirectoryReader(PDF_FOLDER).load_data()
    print(f"✅ {len(documents)} document(s) chargé(s)")
    return documents


# === CRÉATION DE L'INDEX ===
@st.cache_resource
def creer_index():
    documents = charger_documents()
    print("🟣 Création de l'index vectoriel...")

    # Modèle pour répondre aux questions (LLM)
    llm = Ollama(model=MODEL_NAME, request_timeout=120.0)

    # Modèle pour créer les vecteurs (embeddings) - DIFFÉRENT du LLM
    embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME)

    Settings.llm = llm
    Settings.embed_model = embed_model

    index = VectorStoreIndex.from_documents(documents)
    print("✅ Index créé avec succès")
    return index


# === DÉMARRAGE ===
with st.spinner("Chargement des PDF et création de l'index..."):
    index = creer_index()

st.success("✅ Agent prêt ! Pose ta question ci-dessous.")

# === INITIALISATION DE L'HISTORIQUE ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# === AFFICHAGE DE L'HISTORIQUE ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === ZONE DE QUESTION ===
if question := st.chat_input("Pose ta question sur les PDF..."):
    # Message utilisateur
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        with st.spinner(" Réflexion en cours..."):
            query_engine = index.as_query_engine()
            response = query_engine.query(question)
            reponse_texte = str(response)
            st.markdown(reponse_texte)

    st.session_state.messages.append({"role": "assistant", "content": reponse_texte})
