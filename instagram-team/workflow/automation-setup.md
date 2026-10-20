# 自動投稿の準備(Instagram API・Instagramログイン版)

ステータス: 準備中。手順1〜4は完了(2026-10-20)。手順5(環境設定)待ち。出典は第三者の解説(Metaの公式ドキュメントは未確認)。画面の名前は変わることがある

## 全体の流れ
| # | やること | 担当 | 状態 |
|---|---|---|---|
| 1 | Instagramがプロアカウント(クリエイター)か確認 | 本人 | 完了(kurashi_kaimono、クリエイター) |
| 2 | Meta for Developers(developers.facebook.com)に登録 | 本人 | 完了 |
| 3 | アプリを作成し、「Instagram」製品を追加(Instagramログイン版のAPI) | 本人(Claudeが画面ごとに案内) | 完了(アプリ kurashi-auto-post、権限 basic・content_publish・(任意)manage_insights、kurashi_kaimonoをInstagramテスターとして承認済み) |
| 4 | 「API setup with Instagram business login」で自分のアカウントを追加し、トークンを発行 | 本人 | 完了(同意画面でコンテンツ公開・インサイトのみ許可) |
| 5 | クラウド環境の設定: ネットワークで `graph.instagram.com` を許可、トークンを環境変数 `IG_ACCESS_TOKEN` に入れる | 本人 | 未 |
| 6 | 新しいセッションを開き、`python3 instagram-team/tools/ig_publish.py check` で接続を確認 | Claude | 未 |
| 7 | テスト投稿1本(本人の承認後)。動画URLの形式が受け付けられるかを確認 | Claude | 未 |
| 8 | 予約の仕組み(スケジュール実行)を作り、`ig_publish.py due` を投稿時刻に実行 | Claude | 未 |

## 安全のルール
- トークンは会話・ファイル・GitHubに書かない。環境の秘密設定(環境変数)にだけ入れる
- 投稿するのは `reels/schedule.json` で `approved: true` のものだけ(本人の週次OKで true にする)
- `mode: "manual"` は本人がアプリで予約した投稿。二重投稿を防ぐため自動投稿しない

## 未確認の点
- 自分のアカウントだけに投稿する場合、Metaのアプリ審査なしで使えるか(開発モードで役割のあるアカウントは使えるとする解説と、審査が必要とする解説がある)
- 長期トークンの有効期限(60日とする解説が多い)と更新の自動化
- 動画URL: GitHubのraw URLは `content-type: application/octet-stream` で配信される。Instagramが受け付けない場合は、GitHub Pages など動画として配信できる場所に切り替える
- 1日の投稿上限(25件または50件とする解説がある)

## 参考(第三者の解説)
- https://gist.github.com/jameschapman2c/65eff9f54a2d350b17a6ce5127b9fe42
- https://www.postzen.dev/blog/how-to-get-instagram-access-token
- https://www.outstand.so/blog/instagram-reels-stories-api

## 新しいセッションでClaudeがやること(引き継ぎ)
1. `echo ${IG_ACCESS_TOKEN:+set}` でトークンが入っているか確認(値は表示しない)
2. `python3 instagram-team/tools/ig_publish.py check` で接続確認。失敗したらネットワーク許可(graph.instagram.com)を確認
3. 本人の承認を得てテスト投稿1本。動画URL(raw.githubusercontent.com)が受け付けられるか確認
4. 投稿時刻に `ig_publish.py due` を実行する予約の仕組みを作り、結果をコミットしてpush
5. トークンの期限(60日とされる)の前に更新する方法を調べて手順化
