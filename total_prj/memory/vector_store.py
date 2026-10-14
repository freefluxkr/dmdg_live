#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
의미망 도서관 (Vector Store): 장기 기억(Long-term Memory)을 저장하고 유사 맥락을 즉시 인출하는 벡터 데이터베이스
"""

import math
import re
import json
from typing import List, Dict, Any, Tuple

class SimpleVectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.vectors: List[List[float]] = []

    def _tokenize(self, text: str) -> List[str]:
        # 한글 및 영숫자 형태소/토큰 추출
        return re.findall(r'[가-힣a-zA-Z0-9_-]+', text.lower())

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        self.documents.extend(docs)
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        if not self.documents:
            return

        doc_tokens = []
        df: Dict[str, int] = {}
        total_docs = len(self.documents)

        for doc in self.documents:
            full_text = f"{doc.get('title', '')} {doc.get('content', '')} {' '.join(doc.get('keywords', []))}"
            tokens = self._tokenize(full_text)
            unique_tokens = set(tokens)
            doc_tokens.append(tokens)
            for t in unique_tokens:
                df[t] = df.get(t, 0) + 1

        # 단어 사전 구축
        all_terms = sorted(list(df.keys()))
        self.vocabulary = {term: idx for idx, term in enumerate(all_terms)}

        # IDF 계산: log(1 + N / (df + 1)) + 1
        self.idf = {term: math.log((1 + total_docs) / (df[term] + 1)) + 1.0 for term in all_terms}

        # 문서별 TF-IDF 벡터 생성 및 정규화
        self.vectors = []
        dim = len(self.vocabulary)
        for tokens in doc_tokens:
            vec = [0.0] * dim
            tf: Dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            for term, count in tf.items():
                if term in self.vocabulary:
                    idx = self.vocabulary[term]
                    vec[idx] = (count / len(tokens)) * self.idf[term]

            # L2 정규화
            norm = math.sqrt(sum(v * v for v in vec))
            if norm > 0:
                vec = [v / norm for v in vec]
            self.vectors.append(vec)

    def search(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        if not self.vectors:
            return []

        tokens = self._tokenize(query)
        dim = len(self.vocabulary)
        q_vec = [0.0] * dim
        tf: Dict[str, int] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        for term, count in tf.items():
            if term in self.vocabulary:
                idx = self.vocabulary[term]
                q_vec[idx] = (count / max(1, len(tokens))) * self.idf[term]

        q_norm = math.sqrt(sum(v * v for v in q_vec))
        if q_norm == 0:
            return [(self.documents[i], 0.0) for i in range(min(top_k, len(self.documents)))]
        q_vec = [v / q_norm for v in q_vec]

        # 코사인 유사도 연산
        scores = []
        for i, doc_vec in enumerate(self.vectors):
            dot = sum(q_vec[j] * doc_vec[j] for j in range(dim))
            scores.append((self.documents[i], float(dot)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

def load_default_vector_store(corpus_path: str) -> SimpleVectorStore:
    vstore = SimpleVectorStore()
    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    vstore.add_documents(corpus)
    return vstore

if __name__ == "__main__":
    import os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_corpus.json")
    vs = load_default_vector_store(sample_path)
    res = vs.search("태풍으로 부산항 침수 시 배터리 대체 공급", top_k=2)
    print("Vector Store Test Result:")
    for doc, score in res:
        print(f"[{score:.4f}] {doc['title']} -> {doc['content'][:80]}...")
