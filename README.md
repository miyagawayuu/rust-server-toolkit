# Rust Server Toolkit

Rustサーバー管理者向けのCodexプラグイン。日本語の依頼から、サーバー構築、Oxide／CarbonのC#プラグイン修正、JSON設定調整を支援します。

**0.1.0-alpha.1 — 初期アルファ版。** Codex向けスキル3本と、読み取り専用JSON検査ツールを同梱します。実サーバーでのセットアップ・C#コンパイル・ゲーム内動作は未検証です。

## 機能

| スキル | 用途 |
| --- | --- |
| `rust-server-setup` | Linux／Windows／Docker／ホスティングパネルに合わせた構築・更新・接続不良調査 |
| `rust-plugin-repair` | コンパイルエラー・読み込み失敗・フック例外の原因調査とソース修正 |
| `rust-plugin-config` | ソースに基づいた設定キー・単位の確認、候補作成、検査、反映手順 |

本プラグインは、Codexに管理手順を提供するスキル型プラグインです。専用RCONクライアントや常駐管理デーモン、自動C#ビルド環境は含みません。実作業にはCodexが使用できるシェル、ファイル、必要に応じたSSH／ホスティングパネルへのアクセスが必要です。JSON補助ツールはPython 3.10以上で動作し、追加パッケージは不要です。

## インストール

公開後、Codex CLIでこのGitHubリポジトリをマーケットプレイスとして追加します。

```sh
codex plugin marketplace add miyagawayuu/rust-server-toolkit
codex plugin add rust-server-toolkit@personal
```

カタログ識別名は生成ツールの既定値 `personal` です。同名のマーケットプレイスが既にある場合は、上書きせずCodexに表示されるソースを確認してください。

ローカル検証は、リポジトリのルートを指定します。

```sh
codex plugin marketplace add /absolute/path/to/rust-server-toolkit
codex plugin add rust-server-toolkit@personal
```

インストール後、新しいタスクでプラグインを選択して試してください。Codexのバージョン・組織ポリシーによってインストール可否が変わります。

## 依頼例

- 「UbuntuのVPSにRustとCarbonをセットアップしたい。まず起動設定を作って」
- 「この.csとログを確認して、Oxideで発生するコンパイルエラーを直して」
- 「このプラグインの採取倍率を2倍にしたい。ソースを確認して設定変更候補を作って」

設定ファイルと対象プラグインのソースまたは説明書があれば、実サーバー接続前でも作業できます。ログにパスワード、トークン、Webhook URLが含まれていないか確認してください。

## JSON検査

リポジトリのルートから実行します。

```sh
python plugins/rust-server-toolkit/skills/rust-plugin-config/scripts/config_check.py check Plugin.json
python plugins/rust-server-toolkit/skills/rust-plugin-config/scripts/config_check.py diff original.json candidate.json
python -m unittest discover -s tests -v
python scripts/package.py
```

検査ツールは入力を変更せず、差分の値を出力しません。差分のキー名には個人情報が含まれる可能性があります。JSON構文の合格だけではプラグイン側の設定仕様への適合は保証できません。

## 公開と開発

- [リリース手順と検証状況](docs/RELEASE.md)
- [動作評価シナリオ](docs/EVALUATION.md)
- [プライバシー](PRIVACY.md)
- ライセンス: MIT。第三者のRustプラグインやサーバーバイナリは同梱しません。

Facepunch、Oxide、Carbon、OpenAIの公式製品ではありません。
