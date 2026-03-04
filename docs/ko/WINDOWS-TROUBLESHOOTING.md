# Windows 문제 해결 가이드

이 가이드는 Windows 사용자가 CodexSpec을 설치하고 실행할 때 발생하는 일반적인 문제를 해결하는 데 도움이 됩니다.

## 문제: CMD에서 "spawn codexspec access denied" (OSError 5)

### 증상

- CMD에서 `codexspec --version` 또는 `codexspec init` 실행이 "Access denied" 또는 "spawn codexspec access denied (OSError 5)"로 실패
- 동일한 명령이 PowerShell에서 올바르게 작동

### 근본 원인

이는 Windows CMD와 PowerShell이 사용자 환경 변수를 처리하는 방식의 차이로 인해 발생합니다:

1. **PATH 환경 변수 새로고침**: uv가 codexspec을 설치할 때 `%USERPROFILE%\.local\bin`을 사용자 PATH에 추가합니다. PowerShell은 일반적으로 이를 즉시 인식하지만, CMD는 터미널이 다시 시작될 때까지 환경 변수를 새로고침하지 않을 수 있습니다.

2. **프로세스 생성 차이**: CMD는 Windows CreateProcess API를 사용하는 반면, PowerShell은 경로 해결 문제에 더 관대할 수 있는 다른 메커니즘을 사용합니다.

### 해결책

#### 해결책 1: PowerShell 사용 (권장)

가장 간단한 해결책은 CMD 대신 PowerShell을 사용하는 것입니다:

```powershell
# PowerShell에서 codexspec 설치 및 실행
uv tool install codexspec
codexspec --version
```

#### 해결책 2: CMD 다시 시작

모든 CMD 창을 닫고 새 창을 엽니다. 이렇게 하면 CMD가 환경 변수를 다시 로드합니다.

#### 해결책 3: CMD에서 PATH 수동 새로고침

```cmd
# 현재 세션에 uv의 bin 디렉토리를 PATH에 추가
set PATH=%PATH%;%USERPROFILE%\.local\bin

# 확인
codexspec --version
```

#### 해결책 4: 전체 경로 사용

```cmd
# 전체 경로를 사용하여 codexspec 실행
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### 해결책 5: 시스템 PATH에 영구적으로 추가

1. **시스템 속성** → **환경 변수** 열기
2. **사용자 변수** 또는 **시스템 변수**에서 `Path` 찾기
3. 추가: `%USERPROFILE%\.local\bin`
4. 확인 클릭 및 모든 터미널 다시 시작

#### 해결책 6: uv tool 대신 pipx 사용

uv에 계속 문제가 있는 경우 pipx를 대안으로 사용:

```cmd
# pipx 설치
pip install pipx
pipx ensurepath

# CMD 다시 시작, 그 다음 codexspec 설치
pipx install codexspec

# 확인
codexspec --version
```

## 확인 단계

문제를 진단하려면 CMD에서 다음 명령을 실행합니다:

```cmd
# uv의 bin 디렉토리가 PATH에 있는지 확인
echo %PATH% | findstr ".local\bin"

# codexspec 실행 파일이 존재하는지 확인
dir %USERPROFILE%\.local\bin\codexspec.*

# 전체 경로로 실행 시도
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## 일반적인 문제

### 문제: "uv is not recognized"

**원인**: uv가 설치되지 않았거나 PATH에 없습니다.

**해결책**:
```powershell
# PowerShell을 사용하여 uv 설치
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 터미널 다시 시작 및 확인
uv --version
```

### 문제: "python is not recognized"

**원인**: Python이 설치되지 않았거나 PATH에 없습니다.

**해결책**:
1. [python.org](https://www.python.org/downloads/)에서 Python 3.11+ 설치
2. 설치 중에 "Add Python to PATH" 체크
3. 터미널 다시 시작

### 문제: 안티바이러스가 실행 차단

**증상**: Codexspec이 잠시 작동하다가 중지되거나 간헐적인 오류 표시.

**해결책**: codexspec을 안티바이러스 허용 목록에 추가:
- **Windows Defender**: 설정 → 업데이트 및 보안 → Windows 보안 → 바이러스 및 위협 보호 → 설정 관리 → 제외
- 경로 추가: `%USERPROFILE%\.local\bin\codexspec.exe`

## 관련 리소스

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - uv의 알려진 Windows 권한 문제
- [uv Windows 설치 가이드](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx 문서](https://pypa.github.io/pipx/) - 대체 Python 애플리케이션 설치 프로그램
