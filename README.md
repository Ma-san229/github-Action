## ローカル動画からGeminiで文字起こしし、AIニュース記事とポッドキャストを自動生成するCLI

このツールは、ローカルの動画ファイルを入力すると、以下を自動で行います。

- 音声抽出（FFmpeg）
- Gemini API による文字起こし（テキストとSRT）
- 日本語のAIニュース記事生成（見出し・本文・要点）
- TTS によるポッドキャスト音声生成（MP3）

### 使い方（クイック）

1) 依存関係をインストール

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) 環境変数で Gemini API キーを設定

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
```

3) 実行

```bash
python -m app.cli --video /path/to/local_video.mp4 --out out_dir
```

出力物：

- out_dir/audio.wav
- out_dir/transcript.txt
- out_dir/transcript.srt
- out_dir/article.md
- out_dir/podcast.mp3

### 参考文献・出典（Gemini / File API / 音声処理）

- Google AI for Developers: Gemini API（Python SDK）ファイルの取り扱い・`upload_file`（公式）
  - ドキュメント: `https://ai.google.dev/gemini-api/docs/get-started/python?hl=ja`
  - ファイルアップロードの概念/安全性: `https://ai.google.dev/gemini-api/docs/prompting_with_media?hl=ja`

- Python SDK リファレンス（google-generativeai）
  - `https://pypi.org/project/google-generativeai/`

- FFmpeg 公式
  - `https://ffmpeg.org/`

### 参考実装・関連ワークフロー

- KentaHomma/kamuicode-workflow（参考ワークフロー、AIニュース記事生成モジュール v0.4.0 の構成に着想）
  - GitHub: `https://github.com/KentaHomma/kamuicode-workflow`

このプロジェクトでは、上記の公式ドキュメントやワークフローの考え方を参考にしつつ、ローカル動画→文字起こし→ニュース記事→ポッドキャスト生成の一連の処理を、シンプルなCLIとして提供します。

