# Windows トラブルシューティングガイド

このガイドは、Windows ユーザーが CodexSpec のインストールと実行時に発生する一般的な問題を解決するのに役立ちます。

## 問題: CMD で "spawn codexspec access denied" (OSError 5) が発生

### 症状

- CMD で `codexspec --version` または `codexspec init` を実行すると "Access denied" または "spawn codexspec access denied (OSError 5)" で失敗する
- 同じコマンドが PowerShell では正常に動作する

### 原因

これは Windows CMD と PowerShell がユーザー環境変数を処理する方法の違いによって発生します:

1. **PATH 環境変数の更新**: uv が codexspec をインストールすると、`%USERPROFILE%\.local\bin` をユーザー PATH に追加します。PowerShell は通常これを即座に認識しますが、CMD は端末を再起動するまで環境変数を更新しない場合があります。

2. **プロセス作成の違い**: CMD は Windows CreateProcess API を使用しますが、PowerShell はパス解決の問題に対してより寛容な異なるメカニズムを使用します。

### 解決策

#### 解決策 1: PowerShell を使用する (推奨)

最も簡単な解決策は、CMD の代わりに PowerShell を使用することです:

```powershell
# PowerShell で codexspec をインストールして実行
uv tool install codexspec
codexspec --version
```

#### 解決策 2: CMD を再起動する

すべての CMD ウィンドウを閉じて、新しいものを開きます。これにより、CMD は環境変数を強制的に再読み込みします。

#### 解決策 3: CMD で PATH を手動で更新する

```cmd
# 現在のセッションの PATH に uv の bin ディレクトリを追加
set PATH=%PATH%;%USERPROFILE%\.local\bin

# 確認
codexspec --version
```

#### 解決策 4: フルパスを使用する

```cmd
# フルパスを使用して codexspec を実行
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### 解決策 5: システム PATH に永続的に追加する

1. **システムのプロパティ** → **環境変数** を開く
2. **ユーザー環境変数** または **システム環境変数** で `Path` を見つける
3. 追加: `%USERPROFILE%\.local\bin`
4. OK をクリックして、すべての端末を再起動する

#### 解決策 6: uv tool の代わりに pipx を使用する

uv で問題が続く場合は、pipx を代替として使用します:

```cmd
# pipx をインストール
pip install pipx
pipx ensurepath

# CMD を再起動してから、codexspec をインストール
pipx install codexspec

# 確認
codexspec --version
```

## 確認手順

問題を診断するには、CMD で以下のコマンドを実行します:

```cmd
# uv の bin ディレクトリが PATH にあるか確認
echo %PATH% | findstr ".local\bin"

# codexspec 実行ファイルが存在するか確認
dir %USERPROFILE%\.local\bin\codexspec.*

# フルパスで実行してみる
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## 一般的な問題

### 問題: "uv is not recognized"

**原因**: uv がインストールされていないか、PATH にない。

**解決策**:
```powershell
# PowerShell を使用して uv をインストール
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 端末を再起動して確認
uv --version
```

### 問題: "python is not recognized"

**原因**: Python がインストールされていないか、PATH にない。

**解決策**:
1. [python.org](https://www.python.org/downloads/) から Python 3.11+ をインストール
2. インストール時に "Add Python to PATH" をチェック
3. 端末を再起動

### 問題: アンチウイルスが実行をブロック

**症状**: Codexspec が一時的に動作してから停止する、または断続的なエラーが表示される。

**解決策**: codexspec をアンチウイルスの除外リストに追加:
- **Windows Defender**: 設定 → 更新とセキュリティ → Windows セキュリティ → ウイルスと脅威の防止 → 設定の管理 → 除外
- パスを追加: `%USERPROFILE%\.local\bin\codexspec.exe`

## 関連リソース

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - uv に関する既知の Windows 権限問題
- [uv Windows インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx ドキュメント](https://pypa.github.io/pipx/) - 代替 Python アプリケーションインストーラー
