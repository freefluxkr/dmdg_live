def get_recommendation(gender, top_priority):
    print(f"👤 사용자 프로필: 성별=[{gender}], 최우선 고려사항=[{top_priority}]")
    
    if top_priority == '교통':
        if gender == '남자':
            return "👉 추천 거주지: [도심 역세권 오피스텔 또는 빌라]\n이유: 남성 직장인/학생의 경우 치안보다는 출퇴근/통학 시간 단축과 교통 편의성을 극대화할 수 있는 역세권 1인가구 주거지가 가장 만족도가 높습니다."
        else:
            return "👉 추천 거주지: [역세권 대단지 아파트 또는 보안 우수 오피스텔]\n이유: 교통이 중요하지만 여성의 경우 기본적인 치안(안전)도 확보되어야 하므로 대로변에 위치한 보안이 철저한 역세권 거주지를 추천합니다."
            
    elif top_priority == '안전':
        return "👉 추천 거주지: [치안 우수 대단지 아파트]\n이유: 보안 시설과 자체 경비 시스템이 잘 갖춰져 있어 안전을 최우선으로 하는 분께 적합합니다."
        
    elif top_priority == '소음':
        return "👉 추천 거주지: [외곽 조용한 숲세권 전원주택 또는 단독주택]\n이유: 도심의 층간소음이나 차량 소음을 피해 조용하고 쾌적한 환경을 제공합니다."
        
    else:
        return "👉 추천 거주지: [일반 주택단지]\n이유: 무난한 거주 환경을 제공합니다."

if __name__ == "__main__":
    result = get_recommendation('남자', '교통')
    print("-" * 50)
    print(result)
    print("-" * 50)
