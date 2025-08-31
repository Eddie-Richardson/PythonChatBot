# src/memory/kb_store.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from src.config import MEMORY_CONFIG

chroma_dir = MEMORY_CONFIG["chroma_dir"]
_chroma = chromadb.Client(Settings(persist_directory=chroma_dir))
_model = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION = "knowledge_base"

def collection():
    try:
        return _chroma.get_collection(COLLECTION)
    except:
        return _chroma.create_collection(COLLECTION)

def add_docs(workspace: str, docs: list[str], metadatas: list[dict]):
    ids = [f"{workspace}:{i}" for i in range(len(docs))]
    embs = _model.encode(docs).tolist()
    collection().add(documents=docs, embeddings=embs, metadatas=metadatas, ids=ids)
    _chroma.persist()

def search(workspace: str, query: str, k: int = 5):
    emb = _model.encode([query]).tolist()
    res = collection().query(query_embeddings=emb, n_results=k, where={"workspace": workspace})
    hits = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        hits.append({"text": doc, "meta": meta, "score": dist})
    return hits
