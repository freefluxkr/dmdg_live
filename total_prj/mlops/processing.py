#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MLOps 컨베이어 벨트 - 2. 자동 전처리 및 임베딩 (Processing & Drift Detection):
데이터 드리프트(Data Drift)를 상시 감시하고, 정제된 신규 데이터를 벡터 도서관 및 지식 그래프에 자동 증분 반영
"""

import os
import json
import re
from typing import Dict, Any, List, Tuple

class DataProcessingPipeline:
    def __init__(self, raw_events_path: str, vector_store=None, graph_store=None):
        self.raw_events_path = raw_events_path
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.baseline_vocab = {"배터리", "울산", "부산", "남해고속도로", "재고", "공급", "태풍", "카눈", "세종테크"}

    def detect_data_drift(self) -> Dict[str, Any]:
        """최근 수집된 이벤트 로그를 분석하여 데이터 드리프트(새로운 도메인 어휘 및 이상치 패턴) 측정"""
        if not os.path.exists(self.raw_events_path):
            return {"drift_detected": False, "drift_score": 0.0, "reason": "No raw data"}

        recent_tokens = set()
        total_events = 0

        with open(self.raw_events_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                total_events += 1
                text = json.dumps(record.get("payload", {}), ensure_ascii=False)
                tokens = re.findall(r'[가-힣a-zA-Z0-9_-]+', text)
                recent_tokens.update(tokens)

        # 기준 사전 대비 신규 출현 어휘 비율 측정 (드리프트 지표)
        new_tokens = recent_tokens - self.baseline_vocab
        drift_score = len(new_tokens) / max(1, len(recent_tokens))

        is_drift = drift_score > 0.35 or total_events >= 5

        return {
            "drift_detected": is_drift,
            "drift_score": round(drift_score, 4),
            "total_events_analyzed": total_events,
            "new_emerging_terms": list(new_tokens)[:8],
            "recommendation": "야간 스케줄러 재학습(Nightly LoRA) 트리거 권고" if is_drift else "정상 유지"
        }

    def process_and_update_memory(self) -> Dict[str, Any]:
        """신규 수집 데이터를 전처리하여 장기 기억 벡터 DB 및 지식 그래프에 동적 반영"""
        updated_docs = 0
        new_graph_nodes = 0

        if not os.path.exists(self.raw_events_path):
            return {"status": "NO_NEW_DATA"}

        with open(self.raw_events_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                payload = record.get("payload", {})
                
                # 신규 공급사 발견 시 지식 그래프 및 벡터 DB에 즉각 증분 주입
                if record.get("event_type") == "NEW_SUPPLIER_REPORT":
                    supplier_name = payload.get("supplier", "신규협력사")
                    part = payload.get("part", "BAT-NEW")
                    
                    if self.graph_store:
                        node_id = f"Supplier_{supplier_name.replace(' ', '_')}"
                        self.graph_store.graph.add_node(node_id, type="Supplier", label=supplier_name, location="천안")
                        self.graph_store.graph.add_edge(node_id, f"Part_{part}", relation="EMERGING_BACKUP")
                        new_graph_nodes += 1

                    if self.vector_store:
                        new_doc = {
                            "doc_id": f"SOP-AUTO-{record['unix_time']}",
                            "title": f"신규 유망 공급 파트너 {supplier_name} 분석 보고서",
                            "category": "신규_공급망_증분",
                            "content": f"{supplier_name}에서 {part} 모델에 대해 일산 {payload.get('capacity', '300/day')} 공급 능력 확보. 비상 조달 풀에 자동 편입됨.",
                            "keywords": [supplier_name, part, "신규공급사"]
                        }
                        self.vector_store.add_documents([new_doc])
                        updated_docs += 1

        return {
            "status": "PROCESSING_COMPLETED",
            "incremental_vector_docs_added": updated_docs,
            "new_graph_nodes_registered": new_graph_nodes,
            "timestamp": "Now"
        }

if __name__ == "__main__":
    from ingestion import RAW_EVENTS_FILE
    pipeline = DataProcessingPipeline(RAW_EVENTS_FILE)
    print("Drift Detection Result:", pipeline.detect_data_drift())
