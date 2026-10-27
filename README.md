# 🤖 Agent PDF Qwen (Local RAG)

> **Développé à 13 ans par un jeune créateur algérien 🇩🇿**  
> Un agent IA local, privé et puissant pour analyser et discuter avec vos documents PDF.

## 🌟 Pourquoi ce projet ?
J'ai créé cet agent pour démontrer qu'il est possible de construire une solution d'IA avancée, **100% locale et confidentielle**, sans dépendre d'API cloud coûteuses ou de fuites de données. Tout le traitement (vectorisation et génération) reste sur votre machine.

## 🛠️ Stack Technique
- **Langage** : Python 3.10+
- **Interface** : Streamlit (Web UI réactive)
- **Moteur RAG** : LlamaIndex
- **Modèle de génération** : Qwen (via Ollama)
- **Modèle d'embedding** : nomic-embed-text
- **Confidentialité** : 100% Local (Aucune donnée ne quitte l'ordinateur)

## 🚀 Fonctionnalités
- 📄 Ingestion et analyse de **plusieurs PDF simultanément**
- 💬 Chat contextuel précis avec réponses sourcées
- 🔒 **Zéro fuite de données** : idéal pour des documents sensibles
- ⚡ Interface moderne et simple d'utilisation

## 📦 Installation et Lancement

1. Assurez-vous d'avoir **Ollama** installé et en cours d'exécution sur votre machine.
2. Téléchargez les modèles requis via votre terminal :
   ```bash
   ollama pull qwen3.8:latest  # ou la version que vous utilisez
   ollama pull nomic-embed-text
