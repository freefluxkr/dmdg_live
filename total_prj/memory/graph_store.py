#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
의미망 도서관 (Graph DB): 공급망 개체와 관계망을 분석하여 대체 경로와 병목을 추론하는 지식 그래프
"""

import json
import networkx as nx
from typing import Dict, Any, List, Optional

class SupplyChainGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def load_from_json(self, json_path: str) -> None:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 노드 추가
        for node in data.get("nodes", []):
            node_id = node["id"]
            attrs = {k: v for k, v in node.items() if k != "id"}
            self.graph.add_node(node_id, **attrs)

        # 엣지 추가
        for edge in data.get("edges", []):
            src = edge["source"]
            dst = edge["target"]
            attrs = {k: v for k, v in edge.items() if k not in ["source", "target"]}
            self.graph.add_edge(src, dst, **attrs)

    def find_backup_suppliers(self, part_id_suffix: str) -> List[Dict[str, Any]]:
        """특정 부품에 대한 2차/대체 공급사 및 이원화 경로 탐색"""
        backups = []
        for u, v, data in self.graph.edges(data=True):
            if "Part" in v and part_id_suffix in v:
                relation = data.get("relation", "")
                if "BACKUP" in relation or relation == "ALTERNATIVE_FOR":
                    supplier_data = self.graph.nodes[u]
                    backups.append({
                        "supplier_id": u,
                        "supplier_name": supplier_data.get("label", u),
                        "location": supplier_data.get("location", "알 수 없음"),
                        "tier": supplier_data.get("tier", 2),
                        "relation": relation,
                        "capacity": data.get("capacity", "협의 필요")
                    })
        return backups

    def analyze_route_bottleneck(self, origin_supplier: str, destination_plant: str) -> Dict[str, Any]:
        """공급사에서 조립공장까지의 경로 상 기상/재난 병목 노드 분석"""
        try:
            paths = list(nx.all_simple_paths(self.graph, source=origin_supplier, target=destination_plant))
            risk_paths = []
            safe_paths = []

            for path in paths:
                has_hazard = False
                hazard_nodes = []
                for node in path:
                    node_attrs = self.graph.nodes[node]
                    status = node_attrs.get("status", "")
                    if "WARNING" in status or "HAZARD" in status:
                        has_hazard = True
                        hazard_nodes.append((node, node_attrs.get("label", node), status))

                path_labels = [self.graph.nodes[n].get("label", n) for n in path]
                if has_hazard:
                    risk_paths.append({
                        "path_nodes": path,
                        "path_labels": path_labels,
                        "hazards": hazard_nodes
                    })
                else:
                    safe_paths.append({
                        "path_nodes": path,
                        "path_labels": path_labels
                    })

            return {
                "origin": origin_supplier,
                "destination": destination_plant,
                "total_routes_found": len(paths),
                "compromised_routes": risk_paths,
                "viable_safe_routes": safe_paths
            }
        except Exception as e:
            return {"error": str(e), "compromised_routes": [], "viable_safe_routes": []}

    def get_subgraph_summary(self) -> Dict[str, Any]:
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "suppliers": [n for n, d in self.graph.nodes(data=True) if d.get("type") == "Supplier"],
            "parts": [n for n, d in self.graph.nodes(data=True) if d.get("type") == "Part"],
            "plants": [n for n, d in self.graph.nodes(data=True) if d.get("type") == "Plant"]
        }

if __name__ == "__main__":
    import os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "supply_graph.json")
    sg = SupplyChainGraph()
    sg.load_from_json(sample_path)
    print("Graph DB Summary:", sg.get_subgraph_summary())
    backups = sg.find_backup_suppliers("BAT800K")
    print("Backup Suppliers for BAT-800K:", backups)
    bottlenecks = sg.analyze_route_bottleneck("Supplier_Hanlim", "Plant_Ulsan")
    print("Route Bottleneck Analysis:", bottlenecks)
