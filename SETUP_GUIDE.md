# GitHub Repository Secrets 설정 가이드

GitHub Actions가 자동으로 배포를 수행하기 위해서는 다음 API 키들이 보안 저장소(Secrets)에 등록되어 있어야 합니다.

## 📝 필요한 키 목록
다음 키들을 `.env` 파일에서 복사하여 등록하세요.

1. **`GEMINI_API_KEY`**: AI 리포트 생성용
2. **`TAVILY_API_KEY`**: 뉴스 데이터 수집용

---

## 🚀 등록 방법 (단계별)

1. **GitHub 저장소** 페이지로 이동합니다.
2. 상단 메뉴 탭에서 **⚙️ Settings**를 클릭합니다.
3. 왼쪽 사이드바 메뉴에서 **Security** 섹션을 찾습니다.
4. **Secrets and variables**를 클릭하여 펼친 후 **Actions**를 선택합니다.
5. 우측 상단의 **New repository secret** 초록색 버튼을 클릭합니다.
6. 아래 정보를 각각 입력하고 **Add secret** 버튼을 누릅니다.

### 첫 번째 Secret (Gemini)
- **Name**: `GEMINI_API_KEY`
- **Secret**: (`.env` 파일의 GEMINI_API_KEY 값 복사 붙여넣기)

### 두 번째 Secret (Tavily)
- **Name**: `TAVILY_API_KEY`
- **Secret**: (`.env` 파일의 TAVILY_API_KEY 값 복사 붙여넣기)

---

## ✅ 확인 및 재시동
키 등록이 완료되면, 실패했던 GitHub Actions 워크플로우를 다시 실행해야 합니다.

1. 상단 **Actions** 탭 클릭
2. 실패한(또는 진행 중인) **Deploy to GitHub Pages** 워크플로우 클릭
3. 우측 상단 **Re-run jobs** 버튼 클릭 > **Re-run all jobs** 선택

이제 배포가 정상적으로 진행될 것입니다.
