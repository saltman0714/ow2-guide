# OW2 HERO GUIDE（自動更新型）

スマホ対応の非公式Overwatch攻略PWA。

## GitHub Pagesで公開
1. このZIPを展開する（ZIPそのものはアップロードしない）。
2. GitHubの `ow2-guide` リポジトリに、展開した**中身**をそのままアップロードする。隠しフォルダ `.github` も含む。すでに README がある場合は上書きする。
3. `Settings` → `Pages` → `Build and deployment` → `Deploy from a branch` → `main` / `/(root)` → `Save`。
4. `Actions` → `OW2 data auto-update` → `Run workflow` を一度実行する。ヒーロー詳細データが取得される。
5. `Settings` → `Actions` → `General` → `Workflow permissions` を `Read and write permissions` に設定する。既定の `GITHUB_TOKEN` に書き込み権限がない場合のみ必要。
6. 公開URL `https://あなたのGitHubユーザー名.github.io/ow2-guide/` を開く（反映に少し時間がかかることがある）。

## 自動更新の仕様
- GitHub Actionsが毎日日本時間12:17ごろに起動（GitHubの実行遅延あり）。
- [OverFast API](https://overfast-api.tekrop.fr/) からヒーロー一覧、HP、スキルの名称と説明などを日本語で取得して `data/heroes.json` を更新。非公式APIのため停止・遅延の可能性がある。
- [Blizzard公式パッチノート](https://overwatch.blizzard.com/en-us/news/patch-notes/) を確認し、`data/patch.json` に日時と記事見出しを保存。
- **単発ダメージ/DPS/クールダウンの数値は、APIが提供していない場合には空欄。** パッチノートの文章を誤解して自動で数値を書き換えることはしない。
- アンチピック候補の一覧（`data/counters.json`）は暫定の参考リストで、現時点では自動更新されない。
- オフラインでは最後に取得したデータとアプリが使える（初回のオンライン表示後）。

## エラー時
GitHubの `Actions` ページで失敗した実行ログを確認する。APIが一時的にダウンしても前回の正常なJSONは保持される。公開データの更新にはGitHub Pagesの再デプロイが必要。

Blizzard Entertainmentの非公式ファン制作ツール。
