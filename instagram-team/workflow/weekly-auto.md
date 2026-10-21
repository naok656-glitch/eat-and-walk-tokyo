# 毎週の自動制作(定期実行で使う手順書)

本人の包括承認(brand.yaml の standing_approval)に基づき、毎週3本のリールを自動で作り、自動投稿の予約表に登録する。

## 実行のタイミング
- 毎週月曜 8:47(日本時間)に定期実行(予定タスク trig_014AcVZcD1o9CZijE1KQwT1N。初回 2026-10-26)
- 投稿枠: 毎週 水・金・日 の 20:00(日本時間)。schedule.json の最後の投稿より後の、空いている枠から3つを埋める

## 手順(定期実行のセッションが行う)
0. 準備
   - リポジトリ naok656-glitch/eat-and-walk-tokyo のブランチ claude/instagram-automation-team-l6eb5y を使う
   - フォント: 作業用の一時フォルダで `npm install @fontsource/noto-sans-jp@5.0.19`(files/ を render.js に渡す)
   - 読むもの: rules/brand.yaml、rules/compliance.md、roles/roles.md、直近の reels/batch-*.md(テーマの重複を避ける)
1. リサーチ・企画(担当01〜07)
   - ジャンル(暮らし・節約・便利グッズ)と季節に合うテーマを5案 → 3案を選ぶ。直近と同じテーマは避ける
   - 楽天で紹介できる商品がある「選び方・比較」型を優先(まとめページに載せるため)
2. 台本(担当08〜15)
   - 各本 spec.json(6〜8枚、合計約25〜30秒)を作る。形式は既存の reels/*/spec.json と同じ
   - 事実には出典をつけ、確認できない主張は入れない。具体的な金額・統計は出典がある場合だけ
   - NG表現・効果効能・体験談の禁止を守る
3. 制作(担当16〜22)
   - `node instagram-team/tools/render.js <fontDir> <reelDir>` → `sh instagram-team/tools/make_video.sh <reelDir>`(reelDir は絶対パス)
   - スライドを数枚画像で確認(文字のはみ出し・誤字)
4. キャプション(担当24)
   - caption.txt を作る。商品を紹介する回は1行目に「PR」、本文に「方式別(またはテーマ別)のおすすめはプロフィールのリンクから」
5. 予約表とまとめページ
   - reels/schedule.json に3本を追加(approved: true、at は空いている枠の 20:00+09:00)
   - 商品を紹介する回は instagram-team/picks/picks.json にテーマを追加(must_include / exclude を必ず設定)し、`python3 instagram-team/tools/rakuten_picks.py` でページを更新。選ばれた商品名を確認し、取り違えがあれば picks.json の条件を直して再実行
6. 記録
   - reels/batch-<年>w<週>.md に3本の一覧・事実確認表・出典を書く
   - changelog.md に1行追記、コミットして push
7. 報告
   - 3本のテーマ・投稿日時・まとめページの更新内容を短く報告する(通知で本人に届く)

## やらないこと
- 投稿そのもの(毎日20:02の自動投稿に任せる)
- 課金、アカウント設定の変更、他者への連絡
- 出典のない数値・事実、AI人物、ECサイトの商品画像を動画に使うこと
