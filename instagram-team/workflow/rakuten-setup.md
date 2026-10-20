# 楽天の自動化の準備(楽天ウェブサービスAPI+まとめページ)

ステータス: **完了**(2026-10-21)。まとめページ公開中 https://naok656-glitch.github.io/eat-and-walk-tokyo/ 。残りは本人のInstagramプロフィール設定
目的: 楽天ROOMを手で操作せずに、Claudeが商品を検索してアフィリエイトリンク付きの「まとめページ」を作り、Instagramのプロフィールリンクから誘導する

## 本人の作業(1回だけ・合計15〜20分)
| # | やること | 状態 |
|---|---|---|
| 1 | 楽天ウェブサービス(webservice.rakuten.co.jp)に楽天会員でログインし、アプリを新規登録して「アプリID(applicationId)」を取得 | 完了(アプリ名 kurashipicks、Webアプリケーション、許可サイト naok656-glitch.github.io、有効期限2027-10-21) |
| 2 | 楽天アフィリエイトの管理画面で「アフィリエイトID」を確認 | 完了(アプリ画面に表示) |
| 3 | クラウド環境(インスタ活用)の設定: 許可ドメイン openapi.rakuten.co.jp、環境変数 RAKUTEN_APP_ID / RAKUTEN_AFFILIATE_ID / RAKUTEN_ACCESS_KEY | 完了。ネットワークシークレット(accessKeyヘッダー、Authorization Bearer)は通らなかったため、アクセスキーは環境変数でクエリに付ける方式にした |
| 4 | GitHubでこのリポジトリの GitHub Pages をオンにする(まとめページの公開場所) | 完了(ブランチ claude/instagram-automation-team-l6eb5y の /docs) |

## Claudeの作業
1. 楽天商品検索APIで、方式ごとに加湿器を検索し、基準(レビュー件数・評価など)で候補を選ぶ。基準は compliance.md に従って当日決める
2. アフィリエイトリンク付きのまとめページを作り、GitHub Pagesで公開(PR表記を明記)
3. Instagramのプロフィール(リンク欄・自己紹介 版B)の文面を用意。入力は本人
4. 毎週の動画に合わせて、ページに商品を追加

## 接続方法(2026-10-21確認)
- エンドポイント: `https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260701`(20220601 は「API Configuration not found」)
- パラメータ: applicationId, accessKey, affiliateId(すべて環境変数から)、ヘッダー: Referer / Origin = https://naok656-glitch.github.io
- 環境変数は新しいセッションでのみ読み込まれる(既存セッションでは空)

## まとめページの作り方
- テーマは `instagram-team/picks/picks.json`(検索語・必須語・除外語・説明)。選定条件: レビュー100件以上・評価4.0以上・商品名に必須語あり・除外語なし、レビュー件数の多い順に2件
- 生成: 環境変数のある新しいセッションで `python3 instagram-team/tools/rakuten_picks.py` → docs/index.html を push
- 2026-10-21の初回生成で、方式の取り違え・無関係商品(電気毛布欄にモバイルバッテリー)が出たため、商品名フィルタを追加。宣伝文(【】[])は表示から外す

## 決まっていること
- Amazonは Creators API の条件(直近30日で適格売上10件以上。Amazon公式ドキュメント)を満たすまで自動化しない。満たしたら同じ形で追加する
- 楽天ROOMは公式の投稿APIがないため、自動化の対象にしない(URLは brand.yaml に記録済み)
- この環境から楽天のサイトには、2026-10-20時点で接続できない(設定3で許可が必要)

## 明日あわせて設定すること(本人決定 2026-10-20)
- 毎日20:02の自動投稿はこのまま続ける
- 毎週の動画づくり(3本の企画・台本・動画・キャプション→schedule.jsonに登録)も定期実行にする(質問19: 自動にする)
- トークンの期限(約60日とされる)が近づいたら更新する仕組みを調べて組み込む
- 検討: 投稿チェックをGitHub Actionsで動かせば、毎日のチェックにClaudeの使用量がかからない(トークンをGitHubのシークレットに置く必要あり。本人に選んでもらう)

## 明日の始め方
この会話(または新しい会話)で「楽天の設定の続きを教えて」と書けば、この手順書の1番から案内する
