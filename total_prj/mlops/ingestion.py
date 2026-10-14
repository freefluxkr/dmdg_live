#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MLOps 컨베이어 벨트 - 1. 자동 수집기 (Data Ingestion):
실시간 운영 이벤트, 에이전트 처리 결과, 사용자/공장 피드백을 지속적으로 스트리밍 수집하여 데이터 레이크에 적재
"""

import os
import json
import time
from typing import Dict, Any, List

DATA_LAKE_DIR = os.path.join(os.path.dirname(__file__), "data_lake")
os.makedirs(DATA_LAKE_DIR, exist_ok=True)
RAW_EVENTS_FILE = os.path.join(DATA_LAKE_DIR, "raw_events.jsonl")

class DataIngestionStream:
    def __init__(self, output_path: str = RAW_EVENTS_FILE):
        self.output_path = output_path

    def ingest_event(self, event_type: str, payload: Dict[str, Any], feedback_score: float = 1.0) -> Dict[str, Any]:
        """단일 운영 이벤트 및 피드백 수집"""
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "unix_time": time.time(),
            "event_type": event_type,
            "payload": payload,
            "feedback_score": feedback_score  # 1.0(성공), 0.0(실패/개선필요)
        }
        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def simulate_field_stream(self, count: int = 5) -> List[Dict[str, Any]]:
        """현장 센서 및 SCM 운영 피드백 스트리밍 모의 생성 (새로운 배터리 규격 및 이상 기후 이벤트 포함)"""
        sample_scenarios = [
            ("SENSOR_ALERT", {"part": "BAT-800K", "issue": "셀 온도 42도 상승 감지", "hub": "부산1물류"}, 0.95),
            ("SCM_FEEDBACK", {"route": "남해고속도로", "condition": "집중호우로 화물차 40km 서행", "delay_hr": 2.5}, 0.85),
            ("NEW_SUPPLIER_REPORT", {"supplier": "천안 차세대전지(주)", "capacity": "450/day", "part": "BAT-900X"}, 1.0),
            ("DRIFT_SAMPLE", {"keyword": "극단기후", "hazard": "남부 폭설", "affected_lines": ["LINE-EV-ULSAN"]}, 0.70),
            ("USER_RATING", {"decision_quality": "EXCELLENT", "reaction_time_sec": 1.2}, 1.0)
        ]
        ingested = []
        for i in range(min(count, len(sample_scenarios))):
            e_type, payload, score = sample_scenarios[i]
            ingested.append(self.ingest_event(e_type, payload, score))
        return ingested

    def get_ingested_count(self) -> int:
        if not os.path.exists(self.output_path):
            return 0
        with open(self.output_path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())

if __name__ == "__main__":
    stream = DataIngestionStream()
    res = stream.simulate_field_stream(3)
    print(f"Ingested {len(res)} events. Total in Data Lake: {stream.get_ingested_count()}")
