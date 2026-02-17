# tetris-100 ワークフロー定義

**対象リポジトリ**: kaizawasou/tetris-100  
**目的**: Codexが「指示なし」で正しく作業できる運用ルールを定義  
**原則**: このファイルが正史（SoT）。人間もAIも、これに従う。

---

## 🎯 Codexへの指示（最優先）

```
あなた（Codex）がこのリポジトリで作業する時：

1. 必ず最初に WORKFLOW.md（このファイル）を読む
2. agent.md のルールを守る
3. 以下の「実装フロー」を必ず実行する
4. 証跡を ops/logs/ に残す
5. 人間に確認を求めない（自律実行）
```

---

## 📌 役割分担

### GitHub Issue = SoT（Single Source of Truth）

- すべての作業はIssueから始まり、Issueで終わる
- Issueには「目的 / 変更範囲 / DoD」が必ず書かれている
- Issueは"契約"（書いてないことはやらない）

### Codex = 実装担当

- Issueを読む
- 作業計画 → 実装 → テスト → commit → push → close
- 人間は「結果確認」だけ

### 人間（SOU）= 発注者

- やりたいことを日本語で伝える
- ChatGPTにIssue本文を作らせる
- 結果を確認する

---

## 📋 Issue作成ルール

### 最短フロー（推奨）

```
1. SOUがChatGPTに「やりたいこと」を伝える
2. ChatGPTがIssue本文（Markdown）を生成
3. SOUがCodexにIssue本文を渡す
4. Codexが gh コマンドでIssue作成
5. CodexがそのIssueを解決
```

### Issue本文の必須要素

```markdown
## 目的
なぜこの作業をするのか

## 背景
今やる理由

## 変更範囲
どのファイル/機能を変更するか

## 実装タスク
- [ ] タスク1
- [ ] タスク2
- [ ] タスク3

## DoD（完了条件）
何ができたら完了か

## セキュリティ注意
- 秘密値は絶対にコミットしない
- .gitignore の除外対象を確認
```

---

## 🔄 実装フロー（必須9ステップ）

**Codexは以下を"必ず"実行する**:

```
1. Issueを読む（URL確認）
2. 既存コード/README/構成を把握
3. 変更点を最小化して実装
4. テスト実行（pytest -q 等）
5. git status で不要ファイル混入を確認
6. commit（メッセージ規約に従う）
7. push origin/main
8. Issueをclose（コメントに commit SHA を書く）
9. ops/logs/ に証跡ログを作成
```

**絶対に省略しない**

---

## 📝 コミットメッセージ規約

### 基本形式

```
Fix: Issue #<N> <短い要約>
```

### 例

```
Fix: Issue #12 venv+direnv setup
Fix: Issue #8 Z字ブロック実装
Fix: Issue #15 表示/演出の強化
```

### 禁止例

```
❌ update
❌ fix bug
❌ 修正
❌ Issue #12
```

---

## 📊 証跡ログの書き方

### 場所

```
ops/logs/issue<N>_<summary>_<YYYYMMDD>.md
```

### 例

```
ops/logs/issue12_venv_direnv_20260217.md
```

### 内容（最小セット）

```markdown
# Issue #12 証跡ログ

- Issue URL: https://github.com/kaizawasou/tetris-100/issues/12
- 実行日: 2026-02-17
- commit SHA: abc1234

## 実行したコマンド

```bash
python -m venv .venv
echo 'source .venv/bin/activate' > .envrc
direnv allow
```

## テスト結果

PASS

## 重要な判断

.python-version は作成しない（direnv で管理）
```

### 絶対に書かない

- トークン
- 秘密鍵
- パスワード
- 個人情報

---

## 🚨 DNS問題のSOP（緊急用）

### 症状

```
Codexだけが github.com に接続できない
ブラウザ/手元ターミナルはOK
```

### 診断（1コピペ）

```bash
cd ~/Desktop/tetris-100 && \
env | egrep -i '^(http|https|all)_proxy=' || echo "no_proxy_env" && \
dig +time=2 +tries=1 github.com @1.1.1.1 | egrep '^(github.com|;; ANSWER|;; Query|;; timed out)' && \
curl -I --noproxy '*' -m 8 https://github.com | head -n 1 && \
GIT_TRACE=1 GIT_CURL_VERBOSE=1 git ls-remote https://github.com/kaizawasou/tetris-100.git 2>&1 | sed -n '1,35p'
```

### 復旧（順番固定）

```
1. ブラウザで github.com が開けるか確認

2. ブラウザOK かつ 診断OK でも Codex失敗:
   → push は人間のターミナルで実行
     cd ~/Desktop/tetris-100 && git push origin main
   → Issue close はブラウザで実施

3. ブラウザでも開けない:
   → Wi-Fi OFF/ON
   → 回線切替（テザリング）
   → 再試行
```

### 運用ルール

- 同じ症状でDNS設定いじりに再突入しない
- 原因追跡より push/close の完遂を優先

---

## ⚠️ 禁止事項

### 絶対にやってはいけないこと

```
❌ 秘密値をコミット
❌ .env をコミット
❌ トークンをログに書く
❌ コミットメッセージに機密情報
❌ Issueなしで実装
❌ テストなしでpush
❌ 証跡ログなしでclose
```

---

## 🎓 1回のやり取りで1作業

### 原則

```
作業を混ぜない（直列で進める）:

✅ Issue作成（作業A）
✅ 報告（Issue URL / commit SHA）
✅ Issue解決（作業B）
✅ 報告（commit SHA / ログ）
✅ 次のIssue作成（作業C）

❌ Issue作成と解決を同時
❌ 複数Issue を並行処理
```

### 理由

- ログが混ざらない
- エラーが追跡しやすい
- ロールバックが簡単

---

## 📦 Python環境

### venv + direnv

```bash
# 初回セットアップ
python3 -m venv .venv
echo 'source .venv/bin/activate' > .envrc
direnv allow

# 依存インストール
pip install -r requirements.txt

# テスト
pytest -q
```

### ルール

- .venv/ は .gitignore で除外
- requirements.txt で依存管理
- .python-version は使わない（direnv で管理）

---

## 🔄 今後の改善（任意）

### 必要になったら検討

- Makefile（make test 等）
- pre-commit（コミット前チェック）
- pyproject.toml（依存管理強化）
- CI/CD（GitHub Actions）

### 今は不要

小さく確実に進める

---

## 📚 参考資料

- agent.md（このリポジトリのルール）
- README.md（セットアップ手順）
- scripts/quality_gate_min.sh（このリポジトリの品質ゲート）
- ops/logs/（このリポジトリの証跡ログ）

---

**最終更新**: 2026-02-17  
**バージョン**: v1.0  
**作成者**: SOU（実証: tetris-100）
