# リリース

## 0.1.0-alpha.1

- サーバー構築、C#プラグイン修正、設定調整の3スキル。
- 読み取り専用JSON検証・構造差分ツール。
- MITライセンス、Codex互換マニフェストとポータブルマニフェスト。
- Rustサーバー実機検証は未実施。自動修復エンジンやRCON接続機能は未実装。

### 2026-09-15 ローカル検証

- Windows／Python 3.13: JSON補助ツールの8テスト合格。
- 公式 `validate_plugin.py`: 合格。3スキルの `quick_validate.py`: 合格。
- Codex CLIによるローカルマーケットプレイス登録・インストール: 成功。
- 配布ZIPの内容・CRC検査とSHA-256生成: 成功。
- 新規タスクでのスキル選択と実サーバーでの動作評価: 未実施。

## 配布物

`python scripts/package.py` で、許可したファイルだけを含むZIPとSHA-256ファイルを `dist/` に生成します。ZIPルートにプラグインマニフェストとskillsが配置されます。GitHubはソース配布、ZIPはパッケージ検査・提出候補に使用します。

## 安定版に向けた残作業

1. `EVALUATION.md` の各シナリオを実施し結果を記録。
2. OxideとCarbonそれぞれで対象C#プラグインのコンパイル・ロード・実操作を評価。
3. 新規Codexタスクでインストール後のスキル選択を評価。
4. 公開ディレクトリへの提出では、確認済み公開者情報・必要な連絡先・掲載情報を用意。

## 公開ディレクトリ

GitHub Release作成とOpenAIの公開プラグインディレクトリへの掲載は別の工程です。スキルのみのプラグインも提出対象ですが、掲載には提出権限、確認済み公開者ID、審査等が必要です。2026-09-15確認時点。未提出・未承認の状態を掲載済みと表示しません。

一次資料: [Package your plugin](https://developers.openai.com/plugins/build/plugins)、[Submit plugins](https://developers.openai.com/plugins/deploy/submission)。提出時に最新条件を再確認してください。
