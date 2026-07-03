import os
import re
import faiss
import numpy as np
import json
import hashlib
from knowledge_base import knowledge_documents

# Cache directory and files
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
INDEX_PATH = os.path.join(CACHE_DIR, "vector_store.index")
META_PATH = os.path.join(CACHE_DIR, "vector_store_meta.json")

# Linux command expansions/synonyms to improve semantic keyword matching
COMMAND_EXPANSIONS = {
    "whoami": "who am i user",
    "netstat": "network status statistics active connections sockets network connections",
    "ifconfig": "interface configuration network ip address",
    "lscpu": "list cpu architecture processor information",
    "df": "disk free space usage filesystem disk space usage",
    "ps": "process status list running processes active",
    "ss": "socket statistics connections ports",
    "nc": "netcat utility connection listener",
    "uname": "unix name system information kernel OS",
    "chmod": "change mode permissions executable read write",
    "uptime": "system run time load average",
    "top": "system monitor process explorer active task manager",
    "free": "free memory ram swap usage check ram usage ram status",
    "w": "logged in users who active sessions",
    "crontab": "cron jobs scheduler persistence scheduled tasks task manager crontab -l crontab -e",
    "crontab -l": "list cron jobs scheduler scheduler config schedule listing",
    "crontab -e": "edit cron jobs scheduler scheduler config schedule configuration menu",
    "find": "find search locate directories files permissions recursive discovery find file",
    "grep": "grep search pattern match find text string filter print lines matching pattern",
    "hostname": "hostname name network system name host identity",
    "dmesg": "dmesg kernel messages ring buffer system log driver boot logs",
    "docker": "docker container virtualization engine images docker-compose containers status listing",
    "sudo": "sudo superuser do run command as root administrator privileges",
    "iptables": "iptables firewall rules block traffic packet filter administration nat redirect ports",
    "which": "which locate command path bin binary path",
    "lsb_release": "lsb_release distributor id ubuntu release info codename lsb release version",
    "cat": "cat print file contents display read view file raw text cat",
    "last": "last logged in users user history logins pts sessions active system log",
    "history": "history command history list terminal commands run run log list",
    "nmap": "nmap network scanner port scan discovery recon vulnerability audit nmap scan",
    "ping": "ping check host active latency connection icmp echo test network ping",
    "mkdir": "mkdir make directory create directory new folder",
}

index = None
documents = []
vectorizer = None


class TFIDFVectorizer:
    def __init__(self, stopwords=None):
        if stopwords is None:
            self.stopwords = {
                "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
                "with", "is", "of", "it", "this", "that", "these", "those"
            }
        else:
            self.stopwords = stopwords
        self.vocab = {}
        self.idf = []
        self.dimension = 0

    def _tokenize(self, text):
        text = text.lower()
        words = re.findall(r'\b[a-zA-Z0-9_-]+\b', text)
        return [w for w in words if w not in self.stopwords]

    def fit(self, documents_list):
        doc_tokens = [self._tokenize(doc) for doc in documents_list]
        
        vocab = {}
        idx = 0
        for tokens in doc_tokens:
            for token in tokens:
                if token not in vocab:
                    vocab[token] = idx
                    idx += 1
        self.vocab = vocab
        self.dimension = len(vocab)

        df = np.zeros(self.dimension)
        for tokens in doc_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                df[vocab[token]] += 1

        N = len(documents_list)
        self.idf = np.log((1 + N) / (1 + df)) + 1

    def transform(self, text):
        tokens = self._tokenize(text)
        tf = np.zeros(self.dimension)
        for token in tokens:
            if token in self.vocab:
                tf[self.vocab[token]] += 1
        
        tfidf = tf * self.idf
        
        norm = np.linalg.norm(tfidf)
        if norm > 0:
            tfidf = tfidf / norm
        return tfidf.astype("float32")


def get_kb_hash(docs):
    serialized = json.dumps(docs, sort_keys=True)
    return hashlib.md5(serialized.encode('utf-8')).hexdigest()


def build_index():
    global index, documents, vectorizer

    os.makedirs(CACHE_DIR, exist_ok=True)
    kb_hash = get_kb_hash(knowledge_documents)

    texts = []
    for doc in knowledge_documents:
        cmd = doc["command"]
        desc = doc["description"]
        expansion = COMMAND_EXPANSIONS.get(cmd, "")
        # Boost command name matching by repeating it and appending synonyms
        texts.append((cmd + " ") * 3 + (expansion + " ") + desc)

    vectorizer = TFIDFVectorizer()
    vectorizer.fit(texts)

    vectors = []
    for text in texts:
        vectors.append(vectorizer.transform(text))
    
    vectors = np.array(vectors).astype("float32")

    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    meta = {
        "hash": kb_hash,
        "vocab": vectorizer.vocab,
        "idf": vectorizer.idf.tolist(),
        "documents": knowledge_documents
    }
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    documents = list(knowledge_documents)
    print("[Vector Store] Index built and saved successfully.")


def init_vector_store():
    global index, documents, vectorizer

    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        try:
            with open(META_PATH, "r", encoding="utf-8") as f:
                meta = json.load(f)
            
            current_hash = get_kb_hash(knowledge_documents)
            if meta.get("hash") == current_hash:
                index = faiss.read_index(INDEX_PATH)
                documents = meta["documents"]
                
                vectorizer = TFIDFVectorizer()
                vectorizer.vocab = meta["vocab"]
                vectorizer.idf = np.array(meta["idf"])
                vectorizer.dimension = len(vectorizer.vocab)
                
                print("[Vector Store] Index and metadata loaded successfully from cache.")
                return
            else:
                print("[Vector Store] Knowledge base changed. Rebuilding index...")
        except Exception as e:
            print(f"[Vector Store] Error loading cache: {e}. Rebuilding index...")
    
    build_index()


def search(query, threshold=0.0):
    global index, documents, vectorizer

    if index is None or vectorizer is None:
        init_vector_store()

    # Calculate ratio of query tokens that are in vocabulary
    tokens = vectorizer._tokenize(query)
    if tokens:
        first_token = tokens[0]
        # Check if the first token matches any command name in our documents list
        first_token_is_cmd = any(first_token == doc["command"].split()[0] for doc in documents) if documents else False
        
        in_vocab = sum(1 for t in tokens if t in vectorizer.vocab)
        ratio = in_vocab / len(tokens)
        
        # Boost ratio if the query starts with a known command
        if first_token_is_cmd:
            ratio = max(ratio, 0.8)
            
        # Only penalize if vocabulary coverage is less than 50%
        if ratio >= 0.5:
            ratio = 1.0
    else:
        ratio = 0.0

    query_vector = vectorizer.transform(query).astype("float32")
    
    D, I = index.search(np.array([query_vector]), k=1)
    
    idx = I[0][0]
    score = float(D[0][0]) * ratio
    
    if idx != -1 and score >= threshold:
        return documents[idx]
    return None
