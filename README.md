# GCP Workflow Re-execute

Google Cloud Workflows를 Python 클라이언트 라이브러리를 사용하여 재실행하는 도구입니다.

## 요구사항

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (패키지 관리자)
- Google Cloud 프로젝트 및 Workflows API 활성화

## 설치

```bash
uv sync
```

## 환경 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 값을 설정합니다.

```bash
cp .env.example .env
```

### 환경 변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `GOOGLE_CLOUD_PROJECT` | O | GCP 프로젝트 ID |
| `GOOGLE_CLOUD_LOCATION` | O | Workflow 리전 (예: `asia-northeast3`) |
| `WORKFLOW_ID` | O | 실행할 Workflow ID |
| `WORKFLOW_ARGUMENTS` | X | Workflow에 전달할 인자 (JSON 문자열) |
| `GOOGLE_APPLICATION_CREDENTIALS` | X | 서비스 계정 키 파일 경로 |
| `LOG_LEVEL` | X | 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL) |

## 사용 방법

```bash
uv run python main.py
```

## 인증

다음 중 하나의 방법으로 GCP 인증을 설정해야 합니다:

1. `gcloud auth application-default login` 실행
2. `GOOGLE_APPLICATION_CREDENTIALS` 환경 변수에 서비스 계정 키 파일 경로 설정

## Disclaimer

이 프로젝트는 PoC(Proof of Concept) 목적으로 작성되었습니다. 프로덕션 환경에서 사용하기 전에 충분한 테스트와 검토가 필요합니다. 이 코드를 사용하여 발생하는 모든 문제에 대한 책임은 사용자에게 있습니다.

## 참고 자료

- [Google Cloud Workflows Documentation](https://cloud.google.com/workflows/docs)
- [Workflows Python Client Library](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/workflows/cloud-client)
