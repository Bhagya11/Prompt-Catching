# 🚀 Prompt Caching Demo with Ollama (Python)

A minimal Python project demonstrating **application-level prompt caching** using a local Large Language Model (LLM) via Ollama.

The goal of this project is to show how caching repeated prompts can dramatically reduce latency by avoiding unnecessary LLM calls.

---

## ✨ Features

- Run a local LLM with Ollama (`gemma3:1b`)
- Download and clean a long web document
- Send the document to the LLM for summarization
- Measure inference time
- Cache prompt → response in memory
- Instantly return cached results on repeated prompts
- Observe cache hits vs cache misses

> ⚠️ This project demonstrates **response caching at the application layer**, not model-side KV cache or provider-side prompt caching.

