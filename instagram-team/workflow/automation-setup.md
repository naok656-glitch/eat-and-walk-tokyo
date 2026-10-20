# 自動投稿の準備(Instagram API・Instagramログイン版)

ステータス: **稼働中**(2026-10-20)。毎日20:02(日本時間)に定期実行の予定タスク(trig_01TVmZsnw3JxcbyQdZTtPL6F)が ig_publish.py due を実行。出典は第三者の解説(Metaの公式ドキュメントは未確認)。画面の名前は変わることがある

## 全体の流れ
| # | やること | 担当 | 状態 |
|---|---|---|---|
| 1 | Instagramがプロアカウント(クリエイター)か確認 | 本人 | 完了(kurashi_kaimono、クリエイター) |
| 2 | Meta for Developers(developers.facebook.com)に登録 | 本人 | 完了 |
| 3 | アプリを作成し、「Instagram」製品を追加(Instagramログイン版のAPI) | 本人(Claudeが画面ごとに案内) | 完了(アプリ kurashi-auto-post、権限 basic・content_publish・(任意)manage_insights、kurashi_kaimonoをInstagramテスターとして承認済み) |
| 4 | 「API setup with Instagram business login」で自分のアカウントを追加し、トークンを発行 | 本人 | 完了(同意画面でコンテンツ公開・インサイトのみ許可) |
| 5 | クラウド環境(インスタ活用)の「シークレット」に Bearer トークンを追加(許可ウェブサイト `graph.instagram.com`)。接続許可も自動で作られる | 本人 | 完了 |
| 6 | `python3 instagram-team/tools/ig_publish.py check` で接続を確認 | Claude | 完了(kurashi_kaimono / MEDIA_CREATOR、上限100件/24時間。Bearerヘッダーで認証できた) |
| 7 | 動画URLが受け付けられるかを確認 | Claude | 完了(raw.githubusercontent.com の動画でコンテナ作成→FINISHED。投稿はしていない) |
| 8 | 予約の仕組み(スケジュール実行)を作り、`ig_publish.py due` を投稿時刻に実行 | Claude | 完了(毎日20:02 JST。新しいセッションで実行し、投稿したら schedule.json と changelog を push) |

## 安全のルール
- トークンは会話・ファイル・GitHubに書かない。クラウド環境のシークレットにだけ入れる
- 投稿するのは `reels/schedule.json` で `approved: true` のものだけ(本人の週次OKで true にする)
- `mode: "manual"` は本人がアプリで予約した投稿。二重投稿を防ぐため自動投稿しない

## 未確認の点
- 自分のアカウントだけに投稿する場合、Metaのアプリ審査なしで使えるか(開発モードで役割のあるアカウントは使えるとする解説と、審査が必要とする解説がある)
- 長期トークンの有効期限(60日とする解説が多い)と更新の自動化
- 動画URL: GitHubのraw URL(`application/octet-stream`)でも受け付けられた(2026-10-20確認)
- 1日の投稿上限(25件または50件とする解説がある)

## 参考(第三者の解説)
- https://gist.github.com/jameschapman2c/65eff9f54a2d350b17a6ce5127b9fe42
- https://www.postzen.dev/blog/how-to-get-instagram-access-token
- https://www.outstand.so/blog/instagram-reels-stories-api

## 新しいセッションでClaudeがやること(引き継ぎ)
1. トークンはシークレットとして通信時に自動付与される(スクリプトからは見えない)。確認は手順2で行う
2. `python3 instagram-team/tools/ig_publish.py check` で接続確認。失敗したらネットワーク許可(graph.instagram.com)を確認
3. 本人の承認を得てテスト投稿1本。動画URL(raw.githubusercontent.com)が受け付けられるか確認
4. 投稿時刻に `ig_publish.py due` を実行する予約の仕組みを作り、結果をコミットしてpush
5. トークンの期限(60日とされる)の前に更新する方法を調べて手順化
