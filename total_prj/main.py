#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
========================================================================================
🚀 엔터프라이즈 스마트 SCM 자율 운영 에이전트 & 자율 진화 MLOps 플랫폼 (Total Project)
========================================================================================
핵심 5대 구성 요소:
1. 🧠 LLM Brain: 중앙에서 상황을 추론하고 목표를 분해하는 뇌
2. 🛠️ 도구 사용 (Function Calling): 사내 ERP 조회/발주, 기상 특보 API, 비상 이메일 발송
3. 📚 의미망 도서관 (Vector & Graph DB): 장기 기억(Long-term Memory) 및 공급망 지식그래프
4. 🏭 오케스트레이션 공장 (LangGraph StateGraph): 조건부 순환 흐름을 견고한 파이프라인으로 연결
5. 🔄 끊임없이 진화하는 MLOps 컨베이어 벨트 (1.수집 ➔ 2.전처리 ➔ 3.재학습 ➔ 4.무중단 서빙)
========================================================================================
"""

import sys
import os
import time
import json
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# 패키지 경로 추가
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from orchestrator.agent_workflow import SCMAutonomousOrchestrator
from mlops.conveyor_loop import MLOpsConveyorBelt

def run_agent_demonstration():
    print("\n" + "=" * 80)
    print("🧠 [파트 1] 엔터프라이즈 SCM 자율 AI 에이전트 의사결정 파이프라인 가동")
    print("=" * 80)
    
    orchestrator = SCMAutonomousOrchestrator()
    goal = "태풍 카눈 북상에 따른 울산공장 배터리 모듈(BAT-800K) 수급 차질 및 라인 셧다운 방어 조치"

    print(f"🎯 부여된 목표: {goal}\n")
    print("┌" + "─" * 78 + "┐")
    print("│ ⚙️ StateGraph 순환 오케스트레이션 루프 실행 로그 (LangGraph Architecture)    │")
    print("└" + "─" * 78 + "┘")

    step_idx = 1
    def step_monitor(node_name: str, state):
        nonlocal step_idx
        if node_name == "BRAIN":
            print(f"\n[Step {step_idx}] 🧠 BRAIN REASONING NODE (상황 분석 및 목표 분해)")
            print(f"   ├─ 사고(Thought): {state.current_thought}")
            print(f"   └─ 결정(Next Action): {state.next_action} {state.action_input or ''}")
            step_idx += 1
        elif node_name == "TOOL_EXECUTE":
            print(f"   ├─ 🛠️ TOOL EXECUTION NODE (물리적 도구 Function Calling 실행)")
            print(f"   │  └─ 도구: {state.next_action}")
            print(f"   │  └─ 관측 결과: {json.dumps(state.latest_observation, ensure_ascii=False)[:110]}...")
        elif node_name == "MEMORY_RAG":
            print(f"   ├─ 📚 MEMORY RAG NODE (의미망 도서관 Vector & Graph DB 인출)")
            if state.retrieved_memory:
                print(f"   │  └─ Vector 장기기억: 《{state.retrieved_memory[0].get('title', '')}》")
            backups = state.graph_insights.get("backup_suppliers", [])
            if backups:
                print(f"   │  └─ Graph 지식망: 대체 공급사 [{backups[0].get('supplier_name')}] 도출 완료")
        elif node_name == "VERIFY":
            print(f"   └─ ⚖️ VERIFICATION NODE (안전성 및 제약조건 검증 통과 ➔ 순환 루프 지속)")

    final_state = orchestrator.execute_goal(goal, on_step=step_monitor)

    print("\n" + "─" * 80)
    print("🏆 [최종 의사결정 및 자율 집행 결과 브리핑]")
    print("─" * 80)
    print(final_state.final_result)
    print("─" * 80)

    return orchestrator

def run_mlops_demonstration(orchestrator):
    print("\n\n" + "=" * 80)
    print("🔄 [파트 2] 끊임없이 진화하는 MLOps 컨베이어 벨트 (무한 루프 시뮬레이션)")
    print("=" * 80)
    print("AI를 방치하면 발생하는 '데이터 드리프트(Data Drift)'를 자율 치유하는 4단계 무한 루프:\n")
    print("  1. 자동 수집기(Data Ingestion)")
    print("     ➔ 2. 자동 전처리 및 임베딩(Processing & Drift Detection)")
    print("     ➔ 3. 야간 스케줄러 재학습(Nightly LoRA)")
    print("     ➔ 4. 무중단 서빙 배포(CI/CD Zero-Downtime Serving)\n")

    conveyor = MLOpsConveyorBelt(
        vector_store=orchestrator.vector_store,
        graph_store=orchestrator.graph_store
    )

    # 1회차 사이클 실행
    conveyor.run_single_cycle(cycle_num=1)

def run_fastapi_server():
    print("\n🌐 [FastAPI 무중단 서빙 플랫폼 기동]")
    import uvicorn
    from mlops.serving_api import app
    print("  ▶ Swagger 문서: http://127.0.0.1:8092/docs")
    print("  ▶ 헬스체크: http://127.0.0.1:8092/health")
    uvicorn.run(app, host="127.0.0.1", port=8092)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Total Project Runner")
    parser.add_argument("--serve", action="store_true", help="FastAPI 서빙 서버 실행")
    args = parser.parse_args()

    if args.serve:
        run_fastapi_server()
    else:
        orch = run_agent_demonstration()
        run_mlops_demonstration(orch)
        print("\n💡 Tip: 'python main.py --serve' 명령어로 FastAPI 무중단 서빙 API(포트 8092)를 구동할 수 있습니다.")
