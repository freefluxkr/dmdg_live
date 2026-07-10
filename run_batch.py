import os
import sys
import subprocess

def run_batch():
    # 처리할 학생 파일 리스트 정의
    students_files = [
        {
            "path": os.path.join("학생들", "어창선_지원서류_v10.pdf"),
            "student": "어창선"
        },
        {
            "path": os.path.join("학생들", "송지현 포트폴리오.260625_1.pdf"),
            "student": "송지현"
        },
        {
            "path": os.path.join("학생들", "포트폴리오_한정현_통합본_수정중.pdf"),
            "student": "한정현"
        }
    ]

    print("=" * 60)
    print("🚀 3명의 학생 포트폴리오 피드백 일괄 생성 시작")
    print("=" * 60)

    # API 키 확인
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ 에러: 환경 변수 'GEMINI_API_KEY'가 설정되지 않았습니다.")
        print("👉 터미널에서 API 키를 먼저 설정하고 스크립트를 재실행해 주세요.")
        print("   예 (PowerShell): $env:GEMINI_API_KEY=\"your_key_here\"")
        print("   예 (CMD): set GEMINI_API_KEY=your_key_here")
        return

    # 순차적으로 핵심 스크립트 실행
    for sf in students_files:
        path = sf["path"]
        student = sf["student"]
        
        if not os.path.exists(path):
            print(f"⚠️ 경고: '{path}' 파일을 찾을 수 없어 건너뜁니다.")
            continue
            
        print(f"\n👉 [{student}] 학생 포트폴리오 피드백 생성 중...")
        cmd = [
            sys.executable,
            "portfolio_feedback_agent.py",
            path,
            "--student",
            student
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ [{student}] 피드백 생성 완료.")
        except subprocess.CalledProcessError as e:
            print(f"❌ [{student}] 처리 중 오류 발생: {e}")

    print("\n" + "=" * 60)
    print("🎉 일괄 작업이 마무리되었습니다.")
    print("portfolio_feedbacks/ 폴더를 확인해 주세요.")
    print("=" * 60)

if __name__ == "__main__":
    run_batch()
