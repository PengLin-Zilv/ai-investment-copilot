# AI Market Copilot Context

## Goal
Build a personal market intelligence copilot, not a trading advisor.

## Current Flow
mock_news.json -> load_news -> rank_news -> build_digest -> save_digest -> daily_digest.md

## Modules
models.py: defines NewsItem
ingest.py: loads mock news
build_digest.py: turns news into markdown
ranker.py: rank the news in order
main.py: runs the pipeline

## Current Status
Mock news pipeline works.

## Next Build
ranker.py: sort news by importance before digest.