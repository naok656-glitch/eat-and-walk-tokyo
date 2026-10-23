# assets_library（絵で追う動画用 素材庫）

目標 400枚 / **現状 80枚（09のみ完成）**。残り320枚は環境制限のため未取得（下記）。

| フォルダ | 目標 | 現状 | 方法 |
|---|---|---|---|
| 01_money / 02_car / 03_house / 04_job | 20ずつ | 0 | Pixabay・Pexels(実写)+Pollinations(イラスト) |
| 05_izakaya_food / 06_police_legal / 07_city_news | 40ずつ | 0 | 同上 |
| 08_bb_characters | 80 | 0 | BOOTH購入済み素材(お得セット1-4)+コモンズ → 透過webm |
| 09_telop_fukidashi_effect | 80 | **80** | Pillowコード生成（透過PNG 1280x720） |

## 09の中身
黄色+黒フチテロップ24 / 赤・白テロップ8 / 吹き出し24(丸・四角・叫び・雲・ボックス) / 矢印8 / 効果音エフェクト16。
文字は最大8字程度。使用フォント: IPAゴシック（IPA Font License、再配布可）。再生成: `python3 -I assets_library/tools/gen_09_telop.py assets_library/09_telop_fukidashi_effect`

## 未完の理由と再開手順
1. **ネットワーク**: この環境から pixabay.com / api.pexels.com / image.pollinations.ai / commons.wikimedia.org が 403（許可ドメイン外）。Environment設定でこれらを Allowed domains に追加。
2. **キー**: リポジトリ・環境に `.env` が無く、PIXABAY_API_KEY / PEXELS_API_KEY が未設定。`.env` をgit管理外で置く（コミット禁止）。
3. **BB(08)**: BOOTHの有料素材は購入者本人のファイルが必要で、再配布規約もあるため自動取得しません。zipを `08_bb_characters/_incoming/` に置いてください（利用規約で商用・動画利用可か要確認、不可は入れない）。webm化はffmpegで対応します。
4. 再開: `python3 assets_library/tools/fetch_stock.py` → `python3 -I assets_library/tools/build_index.py`

## ルール（素材採用基準）
3秒ルール(1枚=3秒で伝わる単純な絵) / 実写・イラスト・キャラの3種混ぜ / テロップは黄色+黒フチ / BBは動かす / 商用NGは入れない（出典・作者・ライセンスを index.csv に記録）。
