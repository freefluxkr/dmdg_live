#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
도구 레지스트리 (Tool Registry & Function Calling Dispatcher):
LLM이 스스로 판단하여 실행할 수 있도록 도구 스키마를 선언하고 호출을 매핑
"""

from typing import Dict, Any, List
from .tool_implementations import (
    query_erp_inventory,
    create_emergency_purchase_order,
    check_weather_and_routes,
    send_alert_dispatch
)

TOOLS_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "name": "query_erp_inventory",
        "description": "사내 ERP 시스템에서 특정 부품의 현재 재고 수량, 안전재고, 주 공급사 정보를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "part_id": {
                    "type": "string",
                    "description": "조회할 부품 코드 (예: BAT-800K, MCU-3200, RELAY-HV)"
                }
            },
            "required": ["part_id"]
        }
    },
    {
        "name": "check_weather_and_routes",
        "description": "운송 경로 또는 특정 지역(부산, 남해안, 청주 등)의 실시간 기상 특보와 고속도로 통제 상태를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_region": {
                    "type": "string",
                    "description": "점검할 지역 또는 도로명 (예: 부산, 남해안, 청주)"
                }
            },
            "required": ["target_region"]
        }
    },
    {
        "name": "create_emergency_purchase_order",
        "description": "재고 소진 위기 시 사내 ERP에 2차 협력사 긴급 발주(Emergency PO)를 생성 및 자동 접수합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "part_id": {"type": "string", "description": "부품 코드 (예: BAT-800K)"},
                "quantity": {"type": "integer", "description": "긴급 발주 수량"},
                "supplier_name": {"type": "string", "description": "발주 대상 협력사 이름"}
            },
            "required": ["part_id", "quantity", "supplier_name"]
        }
    },
    {
        "name": "send_alert_dispatch",
        "description": "생산 총괄, 공장장, 공급사 담당자에게 긴급 비상 공문 및 안내 메일을 자동 발송합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {"type": "string", "description": "수신자 이메일 또는 부서명"},
                "subject": {"type": "string", "description": "공문/메일 제목"},
                "body": {"type": "string", "description": "공문 상세 내용 및 조치 지시사항"}
            },
            "required": ["recipient", "subject", "body"]
        }
    }
]

def dispatch_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """도구 이름과 인수를 받아 실제 물리적 파이썬 도구를 실행하고 결과를 반환"""
    if tool_name == "query_erp_inventory":
        return query_erp_inventory(arguments.get("part_id", ""))
    elif tool_name == "check_weather_and_routes":
        return check_weather_and_routes(arguments.get("target_region", ""))
    elif tool_name == "create_emergency_purchase_order":
        return create_emergency_purchase_order(
            part_id=arguments.get("part_id", ""),
            quantity=int(arguments.get("quantity", 0)),
            supplier_name=arguments.get("supplier_name", "")
        )
    elif tool_name == "send_alert_dispatch":
        return send_alert_dispatch(
            recipient=arguments.get("recipient", ""),
            subject=arguments.get("subject", ""),
            body=arguments.get("body", "")
        )
    else:
        return {"success": False, "error": f"등록되지 않은 도구명: {tool_name}"}
