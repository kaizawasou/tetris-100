Issue #3: Python仮想環境構築（venv + direnv）

URL: https://github.com/kaizawasou/tetris-100/issues/3

## 目的
- プロジェクトごとに依存関係を分離し、再現性のある開発環境を作る
- 初回セットアップ手順を README に固定し、以後は迷わず環境を立ち上げられる状態にする

## 背景
- 「Pythonの仮想環境は最初に作ること」
- venv と direnv を調べて、ベストな方法を提案し、Issueで管理する（まさる指示）

## 方針（このIssueで決める/作る）
### A) venv
- 採用: Python標準 venv
- 置き場所: リポジトリ直下 `.venv/`
- Gitには含めない（`.gitignore` で除外）
- 依存管理: `requirements.txt`（まずはシンプル運用）

### B) direnv
- 目的: ディレクトリに入ったら自動で `.venv` を有効化
- `.envrc` に `source .venv/bin/activate` を記述
- 初回のみ `direnv allow` が必要（安全のため）

## 実装タスク
- [ ] `direnv` の導入手順を調査（macOS想定 / Homebrew）
- [ ] `.envrc` を追加（`.venv` の activate）
- [ ] `requirements.txt` を追加（pytest等、現状必要なものを明記）
- [ ] README.md に「セットアップ」「実行」「テスト」手順を追加
- [ ] 可能なら `make test` 等の短縮導線も検討（任意）
- [ ] Git commit / push

## 完了条件（DoD）
- [ ] `direnv allow` 後、cd しただけで venv が有効化される
- [ ] `pytest -q` が再現性を持って動く（新規マシン想定）
- [ ] README の手順どおりで環境構築できる

## メモ
- `.python-version` は pyenv 等を使う場合に採用（必要ならこのIssue内で判断）

