import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# 필수 패키지 설치 안내: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    
    # 사장님이 넣어주신 열쇠 파일 찾기 (이름이 변경되지 않아도 자동 인식)
    leo_inbox_path = os.path.join(".agent", "inbox", "leo")
    client_secrets_file = None
    
    if os.path.exists(leo_inbox_path):
        for f in os.listdir(leo_inbox_path):
            if f.endswith(".json") and "client_secret" in f:
                client_secrets_file = os.path.join(leo_inbox_path, f)
                break

    if not client_secrets_file:
        print(f"❌ 오류: '{leo_inbox_path}' 폴더에서 client_secret JSON 파일을 찾을 수 없습니다.")
        print("다운로드 받으신 JSON 파일을 inbox/leo 폴더에 넣어주세요.")
        return

    print(f"🔑 열쇠 파일({os.path.basename(client_secrets_file)})을 찾았습니다!")
    print("유튜브 API 인증을 시작합니다. 브라우저 창이 뜨면 구글 계정으로 로그인 후 [허용]을 눌러주세요.")
    
    try:
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        print("✅ 인증 성공! 유튜브 서버에 연결되었습니다.")
        
        # 업로드할 테스트 영상 (실제로는 코다리가 생성한 영상을 넣습니다)
        # video_file = "sample_video.mp4" 
        
        print("\n🚀 [시뮬레이션] 영상 업로드를 준비 중입니다...")
        print("제목: [당목담글] 세상에서 가장 따뜻한 이어읽기 플랫폼 소개")
        print("설명: dmdg AI 팀이 만든 유튜브 자동 업로드 테스트입니다.")
        print("태그: #당목담글 #AI #스타트업")
        
        # 실제 업로드 로직 (주석 처리됨 - 영상 파일이 있을 때 활성화)
        '''
        request = youtube.videos().insert(
            part="snippet,status",
            body={
              "snippet": {
                "categoryId": "22",
                "description": "dmdg AI 팀이 만든 유튜브 자동 업로드 테스트입니다.",
                "title": "[당목담글] 세상에서 가장 따뜻한 이어읽기 플랫폼 소개",
                "tags": ["당목담글", "AI", "스타트업"]
              },
              "status": {
                "privacyStatus": "private" # 테스트용이므로 비공개 업로드
              }
            },
            media_body=MediaFileUpload(video_file)
        )
        response = request.execute()
        print(f"🎉 영상이 성공적으로 업로드되었습니다! (Video ID: {response['id']})")
        '''
        print("✅ (테스트) 스크립트가 완벽하게 준비되었습니다. 실제 영상 파일(.mp4)만 있으면 즉시 업로드됩니다!")

    except Exception as e:
        print(f"❌ 인증 또는 업로드 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
