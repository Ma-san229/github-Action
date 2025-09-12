from __future__ import annotations

from pathlib import Path
import textwrap
import google.generativeai as genai
import os


ARTICLE_SYSTEM_PROMPT = (
    "あなたは日本語のAIニュース記事編集者です。以下の文字起こしを元に、"
    "事実に忠実で読みやすいニュース記事を作成してください。"
    "フォーマット: タイトル、導入（2-3文）、本文（5-8段落）、要点（箇条書き5項目）。"
    "固有名詞や数値は可能な限り正確に。推測は避け、不確実な箇所はその旨を明記。"
)


def configure_gemini_from_env() -> None:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY is not set")
    genai.configure(api_key=api_key)


def generate_news_article(transcript_text: str, model_name: str = "gemini-1.5-pro") -> str:
    configure_gemini_from_env()
    model = genai.GenerativeModel(model_name)
    prompt = (
        ARTICLE_SYSTEM_PROMPT
        + "\n\n--- 文字起こし ---\n"
        + transcript_text[:200000]
    )
    response = model.generate_content(prompt)
    article = response.text or ""
    return article.strip()


def write_article_markdown(article: str, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.write_text(article, encoding="utf-8")
    return path

