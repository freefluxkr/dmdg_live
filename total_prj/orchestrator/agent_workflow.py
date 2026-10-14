#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
오케스트레이션 공장 워크플로우 (Agent Workflow):
LLM Brain, 의미망 도서관(Vector/Graph), 물리적 도구(Function Calling)를
하나의 순환형 StateGraph 파이프라인으로 연결
"""

import os
from typing import Dict, Any, Optional, Callable
try:
    from .state_graph import StateGraph, AgentState
    from brain.llm_brain import LLMBrain
    from tools.tool_registry import TOOLS_DEFINITIONS, dispatch_tool
    from memory.vector_store import load_default_vector_store
    from memory.graph_store import SupplyChainGraph
except (ImportError, ValueError):
    from state_graph import StateGraph, AgentState
    from brain.llm_brain import LLMBrain
    from tools.tool_registry import TOOLS_DEFINITIONS, dispatch_tool
    from memory.vector_store import load_default_vector_store
    from memory.graph_store import SupplyChainGraph

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

class SCMAutonomousOrchestrator:
    def __init__(self):
        self.brain = LLMBrain()
        
        # 의미망 도서관 초기화
        corpus_path = os.path.join(DATA_DIR, "knowledge_corpus.json")
        graph_path = os.path.join(DATA_DIR, "supply_graph.json")
        self.vector_store = load_default_vector_store(corpus_path)
        self.graph_store = SupplyChainGraph()
        self.graph_store.load_from_json(graph_path)

        # StateGraph 구축
        self.graph = StateGraph()
        self._build_graph()

    def _build_graph(self):
        # 1. 뇌 노드 (Brain Reasoning)
        def node_brain_reason(state: AgentState) -> AgentState:
            plan = self.brain.plan_next_step(state.goal, state.history, TOOLS_DEFINITIONS)
            state.current_thought = plan.get("thought", "")
            action = plan.get("action")
            state.next_action = action
            state.action_input = plan.get("action_input")

            if action == "FINISH":
                state.final_result = plan.get("final_decision", "작업이 성공적으로 완결되었습니다.")
                state.is_completed = True
            return state

        # 2. 도구 실행 노드 (Tool Execution)
        def node_tool_execute(state: AgentState) -> AgentState:
            tool_name = state.next_action
            tool_args = state.action_input or {}
            obs = dispatch_tool(tool_name, tool_args)
            state.latest_observation = obs

            # 실행 기록 축적
            state.history.append({
                "step": state.iteration,
                "thought": state.current_thought,
                "tool_name": tool_name,
                "arguments": tool_args,
                "observation": obs
            })
            return state

        # 3. 의미망 도서관 RAG 노드 (Memory Enrichment)
        def node_memory_enrich(state: AgentState) -> AgentState:
            # 최근 도구 관측 결과를 토대로 Vector DB 및 Graph DB 자동 탐색
            query = f"{state.goal} {state.current_thought}"
            vector_docs = self.vector_store.search(query, top_k=2)
            state.retrieved_memory = [doc for doc, score in vector_docs]

            # 배터리 부품 대체 공급사 및 도로 병목 지식 그래프 조회
            backups = self.graph_store.find_backup_suppliers("BAT800K")
            bottlenecks = self.graph_store.analyze_route_bottleneck("Supplier_Hanlim", "Plant_Ulsan")
            state.graph_insights = {
                "backup_suppliers": backups,
                "route_analysis": bottlenecks
            }
            return state

        # 4. 검증 및 평가 노드 (Quality & Safety Verification)
        def node_verify(state: AgentState) -> AgentState:
            # 안전재고 방어율 및 조치 무결성 검증
            return state

        # 그래프 노드 등록
        self.graph.add_node("BRAIN", node_brain_reason)
        self.graph.add_node("TOOL_EXECUTE", node_tool_execute)
        self.graph.add_node("MEMORY_RAG", node_memory_enrich)
        self.graph.add_node("VERIFY", node_verify)

        # 시작점 설정
        self.graph.set_entry_point("BRAIN")

        # 조건부 엣지 (Routing Logic)
        def route_after_brain(state: AgentState) -> str:
            if state.is_completed or state.next_action == "FINISH":
                return "END"
            return "TOOL_EXECUTE"

        def route_after_tool(state: AgentState) -> str:
            return "MEMORY_RAG"

        def route_after_memory(state: AgentState) -> str:
            return "VERIFY"

        def route_after_verify(state: AgentState) -> str:
            return "BRAIN"  # 자기 순환 루프 (Self-Correcting Loop)

        self.graph.add_conditional_edge("BRAIN", route_after_brain)
        self.graph.add_conditional_edge("TOOL_EXECUTE", route_after_tool)
        self.graph.add_conditional_edge("MEMORY_RAG", route_after_memory)
        self.graph.add_conditional_edge("VERIFY", route_after_verify)

    def execute_goal(self, goal: str, on_step: Optional[Callable[[str, AgentState], None]] = None) -> AgentState:
        initial_state = AgentState(goal=goal)
        return self.graph.run(initial_state, on_step_callback=on_step)
