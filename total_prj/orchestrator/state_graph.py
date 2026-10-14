#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
오케스트레이션 공장 (StateGraph Engine - LangGraph 스타일):
복잡한 조건부 순환 흐름(Cyclic State Machine)을 견고한 노드와 엣지로 연결하여 자율 수행
"""

from typing import Dict, Any, Callable, List, Optional
import time

class AgentState:
    def __init__(self, goal: str):
        self.goal: str = goal
        self.history: List[Dict[str, Any]] = []
        self.current_thought: str = ""
        self.next_action: Optional[str] = None
        self.action_input: Optional[Dict[str, Any]] = None
        self.latest_observation: Optional[Any] = None
        self.retrieved_memory: List[Dict[str, Any]] = []
        self.graph_insights: Dict[str, Any] = {}
        self.final_result: Optional[str] = None
        self.iteration: int = 0
        self.max_iterations: int = 40
        self.is_completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "iteration": self.iteration,
            "current_thought": self.current_thought,
            "next_action": self.next_action,
            "latest_observation": self.latest_observation,
            "is_completed": self.is_completed
        }

class StateGraph:
    def __init__(self):
        self.nodes: Dict[str, Callable[[AgentState], AgentState]] = {}
        self.conditional_edges: Dict[str, Callable[[AgentState], str]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable[[AgentState], AgentState]) -> None:
        self.nodes[name] = func

    def set_entry_point(self, name: str) -> None:
        self.entry_point = name

    def add_conditional_edge(self, source_node: str, condition_fn: Callable[[AgentState], str]) -> None:
        self.conditional_edges[source_node] = condition_fn

    def run(self, initial_state: AgentState, on_step_callback: Optional[Callable[[str, AgentState], None]] = None) -> AgentState:
        if not self.entry_point:
            raise ValueError("Entry point is not set for StateGraph.")

        current_node = self.entry_point
        state = initial_state
        step_counter = 0

        while current_node != "END" and step_counter < state.max_iterations:
            step_counter += 1
            if current_node == self.entry_point:
                state.iteration += 1

            # 노드 함수 실행
            node_func = self.nodes.get(current_node)
            if not node_func:
                raise ValueError(f"Node '{current_node}' not registered in graph.")
            state = node_func(state)

            # 노드 실행 후 콜백 통보
            if on_step_callback:
                on_step_callback(current_node, state)

            if state.is_completed:
                break

            # 다음 전이 노드 결정 (조건부 엣지)
            cond_fn = self.conditional_edges.get(current_node)
            if cond_fn:
                current_node = cond_fn(state)
            else:
                break

        return state
