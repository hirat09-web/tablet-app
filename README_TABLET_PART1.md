# Tablet/PWA Part 1

基準: 2026-08-27 に受領した最新スマホ版 `map-app-main (1).zip`。

## Part 1で追加したもの
- Visualización / Estadísticas / Simulación の3機能ナビゲーション
- Android/iPadを想定したタブレット向けタッチUI
- `manifest.json` とPWAアイコン
- ホーム画面からstandalone表示できるPWA設定
- Service Workerのバージョン更新
- HTMLはonline-first、ローカル地図データはcache-firstにして更新残りを減らす構成
- 既存スマホVisualizationのロジックとデータ構成は維持

## 確認方法
フォルダで `python -m http.server 8000` を実行し、`http://localhost:8000` を開きます。
PWA/Service Workerは `file://` では確認できません。

## 注意
OSM/Esriのオンライン背景は通信時のみです。既存の Offline Satellite とローカルPNG/GeoJSONはオフライン利用の対象です。
StatisticsとSimulationの中身はPart 2以降で実装します。
