# 毎週の自動制作(定期実行で使う手順書)

本人の包括承認(brand.yaml の standing_approval)に基づき、週2回、各回最大4本のリールを自動で作り、自動投稿の予約表に登録する。

## 実行のタイミング
- 毎週 月曜8:47 と 木曜8:43(日本時間)に定期実行(月曜 trig_014AcVZcD1o9CZijE1KQwT1N)
- 投稿枠: **毎日 20:00(日本時間)、1日1本**(2026-10-21 本人決定)。翌日以降で schedule.json に投稿がない日を、早い順に最大4日分埋める
- 本数を1日2本に増やす判断は strategy/experiments.md の基準による(平均視聴の改善を確認してから2週間の比較)

## 手順(定期実行のセッションが行う)
0. 準備
   - リポジトリ naok656-glitch/eat-and-walk-tokyo のブランチ claude/instagram-automation-team-l6eb5y を使う
   - フォント: 作業用の一時フォルダで `npm install @fontsource/noto-sans-jp@5.0.19`(files/ を render.js に渡す)
   - 読むもの: rules/brand.yaml、rules/compliance.md、roles/roles.md、直近の reels/batch-*.md(テーマの重複を避ける)
0.5 成績の確認と改善の判断(担当26・27、事業責任者の判断を兼ねる)
   - `python3 instagram-team/tools/ig_insights.py` で reports/ に週次レポートを作る
   - schedule.json で、予約時刻を過ぎたのに published_media_id が空の投稿がないか確認(あれば投稿失敗。報告の先頭に書く)
   - `instagram-team/strategy/kpi-stage.md` で今の段階を判定し、最優先の指標を1つ決める
   - `instagram-team/strategy/experiments.md` の「未判定」で判定日を過ぎたものを、レポートの数値で判定して結果を書く。今週試す変更(1〜2か所まで)を1行追加する
1. リサーチ・企画(担当01〜07)
   - **最優先: 公開済みのブログ記事を動画にする**。`python3 blog-team/tools/hatena_draft.py list` で公開記事を見て、`instagram-team/reels/from-blog.json` に未記録の記事を1本以上選ぶ。動画の内容は記事の「選び方・比較」部分を図解にする(記事の体験談は、記事に書かれている範囲だけ)。使った記事は from-blog.json に記録する
   - 残りの枠は、ジャンル(暮らし・節約・便利グッズ)と季節に合うテーマを5案 → 選ぶ。直近と同じテーマは避ける
   - 楽天で紹介できる商品がある「選び方・比較」型を優先(まとめページに載せるため)
2. 台本(担当08〜15)
   - 各本 spec.json(6〜8枚、合計約25〜30秒)を作る。形式は既存の reels/*/spec.json と同じ
   - 事実には出典をつけ、確認できない主張は入れない。具体的な金額・統計は出典がある場合だけ
   - NG表現・効果効能・体験談の禁止を守る
3. 制作(担当16〜22)
   - `node instagram-team/tools/render.js <fontDir> <reelDir>` → `sh instagram-team/tools/make_video.sh <reelDir>`(reelDir は絶対パス)
   - スライドを数枚画像で確認(文字のはみ出し・誤字)
3.5 公開前チェック(担当13〜15・22、視聴者レビュー)
   - `instagram-team/strategy/qa-checklist.md` のとおり。高リスクの回だけレビュー役を1人起動する
4. キャプション(担当24)
   - caption.txt を作る。まとめページに関連商品がある回(またはこの制作で追加する回)は、1行目に「PR」、本文に「選び方別のおすすめはプロフィールのリンクから」
5. 予約表とまとめページ
   - reels/schedule.json に作った本数を追加(approved: true、at は空いている日の 20:00+09:00)
   - 商品を紹介する回は instagram-team/picks/picks.json にテーマを追加(must_include / exclude を必ず設定)し、`python3 instagram-team/tools/rakuten_picks.py` でページを更新。選ばれた商品名を確認し、取り違えがあれば picks.json の条件を直して再実行
6. 記録
   - reels/batch-<年>w<週>.md に3本の一覧・事実確認表・出典を書く
   - changelog.md に1行追記、コミットして push
7. 報告
   - 先頭に異常(投稿失敗・データ取得失敗)があれば書く。次に、今の段階と最優先の指標、判定した仮説の結果、3本のテーマ・投稿日時、まとめページの更新を短く報告する(通知で本人に届く)

## やらないこと
- 投稿そのもの(毎日20:02の自動投稿に任せる)
- 課金、アカウント設定の変更、他者への連絡
- 出典のない数値・事実、AI人物、ECサイトの商品画像を動画に使うこと
