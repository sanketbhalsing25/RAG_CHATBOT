# RAG_CHATBOT

# how to run ?

# STEP 1 - create environment 

```bash 
python3.11 -m venv venv
```

```bash
source venv/Source/activate
```

# step 2  install the requirements

```bash
pip install -r requirements.txt
```


# Create a `.env` file in the root directory and add your Pinecone & openai credentials

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

```bash
# run the following command to create index  store embeddings to pinecone
python store_index.py
```

```bash
# Then run the following command
python app.py
```

Then,
```bash
open up localhost:
```


# Techstack Used:

- Python
- Flask
- LangChain
- GPT
- Pinecone










