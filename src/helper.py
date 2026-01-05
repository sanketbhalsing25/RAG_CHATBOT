from langchain_community.document_loaders import PyPDFLoader ,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


def load_pdf_files(Data):
    loader = DirectoryLoader(
        Data,
        glob="*.pdf",
        loader_cls=PyPDFLoader

    )
    documents = loader.load()
    return documents


def filter_minimal_docs(documents: List[Document]) -> List[Document]:
    filtered_docs = []
    for doc in documents:
        scr = doc.metadata.get("source")
        filtered_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": scr}
            )

        )
    return filtered_docs


def text_split(filtered_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
    )
    texts_chunks = text_splitter.split_documents(filtered_docs)
    return texts_chunks



# def openai_embedding():
#     Embedding = OpenAIEmbeddings(
#         model="text-embedding-3-small"

#     )

#     return Embedding



def download_embeddings():
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
        
    )
    return embeddings



