# Agent PDF avec Qwen

Agent IA pour analyser des documents PDF localement, en utilisant **Qwen** (modèle local) et **LlamaIndex**.  
Aucune donnée n'est envoyée sur internet : tout reste sur ton ordinateur.

## Fonctionnalités

- Analyse de plusieurs PDF en même temps
- Interface web simple et moderne (Streamlit)
- 100% local et confidentiel
- Questions/réponses sur le contenu des documents

## Prérequis

- [Python 3.10+](https://www.python.org/downloads/)
- [Ollama](https://ollama.com/) installé et lancé
- Les modèles suivants téléchargés dans Ollama :
  - `qwen3.8:27b` (pour répondre aux questions)
  - `nomic-embed-text` (pour indexer les PDF)

## Installation

1. Clone ce dépôt :
   ```bash
   git clone https://github.com/AnneLeclerc/agent-pdf-qwen.git
   cd agent-pdf-qwen

Pour démarrer, il faut taper dans le terminal de pycharm (ou vscode) et taper :    streamlit run app.py
