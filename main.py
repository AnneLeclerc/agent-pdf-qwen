from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# === CONFIGURATION ===
# Nom de ton modèle Qwen dans Ollama (vérifie avec "ollama list" dans un terminal)
MODEL_NAME = "qwen3.8:27b"
# Chemin vers le dossier contenant tes PDF (modifie selon ton cas)
PDF_FOLDER = "./documents"

# === CONFIGURATION OLLAMA ===
llm = Ollama(model=MODEL_NAME, request_timeout=120.0)
embed_model = OllamaEmbedding(model_name=MODEL_NAME)

Settings.llm = llm
Settings.embed_model = embed_model

# === CHARGEMENT DU PDF ===
print(" Chargement des documents...")
documents = SimpleDirectoryReader(PDF_FOLDER).load_data()
print(f"✅ {len(documents)} document(s) chargé(s)")

# === CRÉATION DE L'INDEX (RAG) ===
print("🧠 Création de l'index vectoriel...")
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# === BOUCLE DE CONVERSATION ===
print("\n🤖 Agent prêt ! Tape 'quitter' pour sortir.\n")
while True:
    question = input("❓ Ta question : ")
    if question.lower() == "quitter":
        print(" À bientôt !")
        break

    print("⏳ Réflexion en cours...")
    response = query_engine.query(question)
    print(f"\n💬 Réponse : {response}\n")
