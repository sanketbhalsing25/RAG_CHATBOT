from flask import Flask, request, jsonify,render_template
from src.helper import download_embeddings
from src.prompt import *
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os


app = Flask(__name__)


load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY



embeddings = download_embeddings()

index_name = "medical-bot"

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name,
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

llm = ChatOpenAI(model_name="gpt-5", temperature=0.2)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human","{input}" ),
    ]
)

quetion_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever,quetion_answer_chain)



@ app.route("/")
def index():
    return render_template('chatbot.html')




@app.route("/get", methods=["POST"])
def chat_response():
    data = request.get_json(silent=True)

    msg = data.get("msg") if data else None

    if not msg or not isinstance(msg, str):
        return jsonify({"answer": "Please enter a valid question."})

    print("User input:", msg)

    response = rag_chain.invoke({"input": msg})

    print("Response:", response["answer"])

    return jsonify({"answer": response["answer"]})






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 




