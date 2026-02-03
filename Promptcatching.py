import time
import requests
from bs4 import BeautifulSoup
import ollama

MODEL = "gemma3:1b"   # <-- you already have this

# -----------------------------
# Fetch and clean web content
# -----------------------------
def fetch_article_content(url, retries=3, content_limit=None):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            if content_limit:
                text = text[:content_limit]

            return text

        except Exception:
            attempt += 1
            print(f"Fetch failed (attempt {attempt}), retrying...")
            time.sleep(2)

    raise RuntimeError("Failed to fetch content")


# -----------------------------
# Non-cached inference
# -----------------------------
def make_non_cached_inference(prompt):
    start = time.time()

    response = ollama.generate(
        model=MODEL,
        prompt=prompt,
    )

    return response["response"], time.time() - start


# -----------------------------
# Cached inference
# -----------------------------
def make_cached_inference(prompt, cache):
    if prompt in cache:
        print("✅ Cache hit")
        return cache[prompt], 0.0

    print("❌ Cache miss")
    start = time.time()

    response = ollama.generate(
        model=MODEL,
        prompt=prompt,
    )

    result = response["response"]
    cache[prompt] = result

    return result, time.time() - start


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    url = "https://www.deeplearningbook.org/contents/intro.html"

    print("Fetching document...")
    content = fetch_article_content(url, content_limit=200000)

    prompt = f"""
<doc>
{content[:8000]}
</doc>

Summarize this document in 5 bullets.
"""

    print("\n--- NON CACHED ---")
    out1, t1 = make_non_cached_inference(prompt)
    print(f"Time: {t1:.2f}s")

    cache = {}

    print("\n--- CACHED (first call) ---")
    out2, t2 = make_cached_inference(prompt, cache)
    print(f"Time: {t2:.2f}s")

    print("\n--- CACHED (second call) ---")
    out3, t3 = make_cached_inference(prompt, cache)
    print(f"Time: {t3:.2f}s")

    print("\n=== RESULT (first 300 chars) ===")
    print(out3[:300])
