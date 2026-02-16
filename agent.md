# Agent Rules - Tetris 100

## 最優先ルール

- 作業開始時に必ず `WORKFLOW.md` を先に読む
- 実装手順・証跡・close手順は `WORKFLOW.md` を正史として従う
- 本ファイルは補足ルール。矛盾時は `WORKFLOW.md` を優先する

---

## このプロジェクトについて

- **目的**: Git習得（100種類のテトリスブロック実装）
- **学習内容**: Issue → 実装 → コミット → Push → PR → マージの流れ

---

## 変更管理

### 全ての変更はGitで管理
```bash
# 変更前
git status
git diff

# コミット
git add .
git commit -m "Fix: Issue #1 L字ブロック実装"

# プッシュ
git push origin main
```

---

## 禁止事項
```
❌ 秘密値のコミット（今回は該当なし）
❌ 大きなバイナリファイルのコミット
❌ コミット前のdiff確認を忘れる
```

---

## ファイル構成
```
tetris-100/
├── blocks/（ブロック実装）
│   ├── l_block.py
│   ├── j_block.py
│   └── ...
├── tests/（テスト）
│   ├── test_l_block.py
│   └── ...
├── agent.md（このファイル）
├── .gitignore
└── README.md
```

---

## Issueドリブン開発

1. GitHubでIssueを作成
2. Codexに「Issue #1を解決して」と指示
3. Codexが実装
4. git commit -m "Fix: Issue #1 ..."
5. git push
6. GitHubでIssueをClose

---

## コミットメッセージ
```
Fix: Issue #1 L字ブロック実装
Add: Issue #2 J字ブロック実装
Update: Issue #3 回転処理改善
```
