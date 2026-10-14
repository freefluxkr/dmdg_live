#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
물리적 도구들 (Tools for Function Calling):
1. 사내 ERP 조회 및 긴급 발주
2. 기상청 날씨 및 고속도로 통제 API
3. 협력사/경영진 긴급 통보 이메일 발송
"""

import json
import os
from typing import Dict, Any, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ERP_FILE = os.path.join(DATA_DIR, "erp_mock.json")

def query_erp_inventory(part_id: str) -> Dict[str, Any]:
    """사내 ERP에서 특정 부품의 현재 재고, 안전재고, 주 공급사 정보를 조회합니다."""
    try:
        with open(ERP_FILE, "r", encoding="utf-8") as f:
            erp = json.load(f)
        for item in erp.get("inventory", []):
            if item["part_id"].upper() == part_id.upper():
                days_left = round(item["current_stock"] / 80.0, 2)
                return {
                    "success": True,
                    "part_id": item["part_id"],
                    "part_name": item["part_name"],
                    "current_stock": item["current_stock"],
                    "safety_stock": item["safety_stock"],
                    "stock_status": item["status"],
                    "estimated_days_remaining": days_left,
                    "supplier": item["primary_supplier"],
                    "location": item["storage_location"]
                }
        return {"success": False, "error": f"부품 ID '{part_id}'를 찾을 수 없습니다."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_emergency_purchase_order(part_id: str, quantity: int, supplier_name: str) -> Dict[str, Any]:
    """사내 ERP에 2차 협력사 긴급 발주(Emergency PO)를 즉시 등록합니다."""
    try:
        with open(ERP_FILE, "r", encoding="utf-8") as f:
            erp = json.load(f)
        
        new_po_id = f"PO-EMERGENCY-{len(erp.get('purchase_orders', [])) + 1:04d}"
        new_order = {
            "po_number": new_po_id,
            "part_id": part_id,
            "quantity": quantity,
            "supplier_name": supplier_name,
            "status": "APPROVED_EMERGENCY_DISPATCH",
            "created_at": "2026-10-14 15:30 (Auto-Agent Execution)"
        }
        erp.setdefault("purchase_orders", []).append(new_order)
        
        # 파일 업데이트
        with open(ERP_FILE, "w", encoding="utf-8") as f:
            json.dump(erp, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "po_number": new_po_id,
            "part_id": part_id,
            "quantity": quantity,
            "supplier": supplier_name,
            "message": f"긴급 발주 {new_po_id}가 ERP에 성공적으로 승인 및 접수되었습니다."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_weather_and_routes(target_region: str) -> Dict[str, Any]:
    """지정된 지역 및 주요 고속도로의 실시간 기상 특보와 도로 통제 상태를 조회합니다."""
    region_lower = target_region.lower()
    if "부산" in target_region or "남해" in target_region or "busan" in region_lower:
        return {
            "success": True,
            "region": "부산·남해안 일대",
            "weather_condition": "태풍 '카눈' 근접에 따른 태풍경보 발령",
            "wind_speed_ms": 32.5,
            "rainfall_mm": 180,
            "route_status": {
                "남해고속도로": "침수 및 강풍으로 대형 화물차 통행 전면 통제 중",
                "부산항신항 배후도로": "선박 접안 중단 및 컨테이너 반출입 일시 중단"
            },
            "risk_level": "SEVERE_CRITICAL"
        }
    elif "청주" in target_region or "중부" in target_region or "경부" in target_region:
        return {
            "success": True,
            "region": "충북 청주 및 경부축",
            "weather_condition": "구름 많음 / 강우 없음",
            "wind_speed_ms": 4.1,
            "rainfall_mm": 0,
            "route_status": {
                "경부고속도로": "원활 (전 구간 정상 소통 가능)"
            },
            "risk_level": "NORMAL"
        }
    else:
        return {
            "success": True,
            "region": target_region,
            "weather_condition": "정상 운행 가능",
            "risk_level": "LOW"
        }

def send_alert_dispatch(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """경영진, 공장장, 협력사 담당자에게 긴급 비상 공문 및 SMS/이메일을 전송합니다."""
    return {
        "success": True,
        "recipient": recipient,
        "subject": subject,
        "body_preview": body[:120] + ("..." if len(body) > 120 else ""),
        "dispatch_status": "SENT_DELIVERED",
        "timestamp": "2026-10-14 15:32:00"
    }
