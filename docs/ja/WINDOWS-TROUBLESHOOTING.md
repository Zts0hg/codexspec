# Windows トラブルシューティングガイド

このガイドは、Windows ユーザーが CodexSpec のインストールや実行時に遭遇する一般的な問題を解決するのに役立ちます。

## 問題: CMD で "spawn codexspec access denied" (OSError 5) が発生

### 症状

- CMD で `codexspec --version` や `codexspec init` を実行すると "Access denied" や "spawn codexspec access denied (OSError 5)" で失敗する
- 同じコマンドが PowerShell では正しく動作する

### 根本原因

これは、Windows の CMD と PowerShell でユーザー環境変数の扱いが異なるために起こります。

1. **PATH 環境変数のリフレッシュ**: uv が codexspec をインストールすると、`%USERPROFILE%\.local\bin` をユーザーの PATH に追加します。PowerShell は通常これを即座に認識しますが、CMD はターミナルを再起動するまで環境変数をリフレッシュしないことがあります。

2. **プロセス生成の違い**: CMD は Windows の CreateProcess API を使う一方、PowerShell は別の仕組みを使い、パス解決の問題に対してより寛容な場合があります。

### 解決策

#### 解決策 1: PowerShell を使う (推奨)

もっとも簡単な解決策は、CMD の代わりに PowerShell を使うことです。

```powershell
# PowerShell で codexspec をインストールして実行
uv tool install codexspec
codexspec --version
```

#### 解決策 2: CMD を再起動する

すべての CMD ウィンドウを閉じて、新しいものを開いてください。これにより CMD は環境変数を再読み込みします。

#### 解決策 3: CMD で PATH を手動リフレッシュする

```cmd
# 現在のセッションに対して uv の bin ディレクトリを PATH に追加
set PATH=%PATH%;%USERPROFILE%\.local\bin

# 確認
codexspec --version
```

#### 解決策 4: フルパスを使う

```cmd
# フルパスで codexspec を実行
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### 解決策 5: システムの PATH に恒久的に追加

1. **システムのプロパティ** → **環境変数** を開く
2. **ユーザー環境変数** または **システム環境変数** の中の `Path` を見つける
3. 追加: `%USERPROFILE%\.local\bin`
4. OK をクリックし、すべてのターミナルを再起動

#### 解決策 6: uv の代わりに pipx を使う

uv で問題が続く場合は、代替として pipx を使います。

```cmd
# pipx をインストール
pip install pipx
pipx ensurepath

# CMD を再起動してから codexspec をインストール
pipx install codexspec

# 確認
codexspec --version
```

## 検証手順

問題を診断するために、CMD で次のコマンドを実行します。

```cmd
# uv の bin ディレクトリが PATH にあるか確認
echo %PATH% | findstr ".local\bin"

# codexspec の実行ファイルが存在するか確認
dir %USERPROFILE%\.local\bin\codexspec.*

# フルパスで実行してみる
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## よくある問題

### 問題: "uv is not recognized"

**原因**: uv がインストールされていないか、PATH に入っていません。

**解決策**:

```powershell
# PowerShell を使って uv をインストール
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# ターミナルを再起動して確認
uv --version
```

### 問題: "python is not recognized"

**原因**: Python がインストールされていないか、PATH に入っていません。

**解決策**:

1. [python.org](https://www.python.org/downloads/) から Python 3.11+ をインストール
2. インストール時に "Add Python to PATH" にチェックを入れる
3. ターミナルを再起動

### 問題: アンチウイルスが実行をブロックする

**症状**: codexspec が一瞬動いて止まる、あるいは断続的なエラーが出る。

**解決策**: codexspec をアンチウイルスの除外リストに追加します。

- **Windows Defender**: 設定 → 更新とセキュリティ → Windows セキュリティ → ウイルスと脅威の防止 → 設定の管理 → 除外
- 追加するパス: `%USERPROFILE%\.local\bin\codexspec.exe`

## 関連リソース

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - uv の Windows での既知の権限問題
- [uv Windows インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)
- [pipx ドキュメント](https://pypa.github.io/pipx/) - 代替の Python アプリケーションインストーラ
