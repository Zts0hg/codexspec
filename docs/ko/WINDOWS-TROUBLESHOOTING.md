# Windows 문제 해결

## 설치 확인

PowerShell에서 실제로 사용하는 실행 파일을 확인하고 CLI가 시작되는지 점검하세요. 버전 확인 명령은 `codexspec version`입니다.

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## 명령을 찾을 수 없는 경우

uv가 없으면 설치 안내를 따르세요. uv로 CodexSpec을 설치했지만 `PATH`에 없다면 실행 파일 디렉터리를 확인하고 셸 설정을 갱신한 뒤 새 터미널을 여세요. 어시스턴트가 이전 환경을 물려받았다면 어시스턴트도 다시 시작합니다. 실제 디렉터리는 기본값과 다를 수 있으므로 uv가 알려 주는 경로를 사용하세요.

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## 접근 거부 또는 시작 실패

접근 거부 메시지만으로 원인을 알 수는 없습니다. 정확한 명령, 실행 파일 경로, 오류와 버전을 기록하세요. 파일 존재 여부, 다른 설치가 먼저 선택되는지, 파일 권한이나 보안 소프트웨어가 실행을 막았는지 확인합니다. 관리되는 장치에서는 조직에서 승인한 관리자 지원 절차를 따르세요. PowerShell과 CMD를 비교하는 목적은 환경 차이를 좁히는 것이며, 셸을 바꿨다고 근본 원인이 해결되었다고 가정해서는 안 됩니다.

CLI가 정상 작동하면 원하는 어시스턴트 통합을 지정해 선택한 프로젝트를 초기화하세요. 사전 조건과 프로젝트 갱신 동작은 설치 안내를 참고하세요.

[CodexSpec](getting-started/installation.md)
