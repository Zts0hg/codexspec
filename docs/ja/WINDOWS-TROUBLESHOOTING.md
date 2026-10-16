# Windows のトラブルシューティング

## インストールの確認

PowerShell で実際に使われている実行ファイルを調べ、CLI が起動するか確認します。バージョン確認には `codexspec version` を使います。

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## コマンドが見つからない場合

uv がない場合はインストールガイドに従ってください。uv で CodexSpec をインストール済みなのに `PATH` にない場合は、実行ファイルのディレクトリを確認し、シェル設定を更新して新しいターミナルを開きます。アシスタントが古い環境を引き継いでいる場合はそちらも再起動します。ディレクトリは既定値と異なることがあるため、uv が表示するパスを使ってください。

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## アクセス拒否や起動失敗

アクセス拒否のメッセージだけでは原因を特定できません。正確なコマンド、実行ファイルのパス、エラー、バージョンを記録してください。ファイルの存在、別のインストールが優先されていないか、ファイル権限やセキュリティソフトが実行を妨げていないかを確認します。管理対象の端末では、組織で承認された管理者サポートの手順を使います。PowerShell と CMD の比較は環境差を絞り込むためのもので、シェルを変えれば根本原因が解決するとは限りません。

CLI が動作したら、希望するアシスタント連携を指定して対象プロジェクトを初期化します。前提条件や既存プロジェクトの更新についてはインストールガイドを参照してください。

[CodexSpec](getting-started/installation.md)
