# Perplexity Research Skill

This skill enables the use of the Perplexity API for powerful research and real-time web search capabilities.

## How to Use the Perplexity API for Research

The Perplexity API is ideal for tasks that require up-to-date information, citations, and in-depth research. It can be used to answer questions, summarize articles, and find sources on a given topic.

To use the API, you will need a Perplexity API key, which should be stored in the `PERPLEXITY_API_KEY` environment variable.

## Python Code Examples

Here is a Python code example demonstrating how to use the Perplexity API:

```python
import os
import requests

def perplexity_search(query):
    """
    Performs a search using the Perplexity API.
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

    url = "https://api.perplexity.ai/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for bad status codes

    return response.json()

if __name__ == "__main__":
    try:
        results = perplexity_search("What are the latest advancements in AI-powered code generation?")
        print(results)
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"An error occurred: {e}")
```

## Integration with the Smart AI Router

A smart AI router can be used to determine the best AI model for a given task. Here's how to decide between Perplexity and OpenRouter:

-   **Perplexity:** Use for real-time web search, questions that require citations, and deep research tasks. Perplexity excels at providing accurate, up-to-date information with sources.
-   **OpenRouter:** Use for code generation, creative writing, reviews, and other tasks that do not require real-time web access. OpenRouter provides access to a wide variety of models, each with its own strengths.

### When to Use Perplexity vs. OpenRouter

| Task                      | Recommended Engine | Reasoning                                                                                             |
| :------------------------ | :----------------- | :---------------------------------------------------------------------------------------------------- |
| Real-time web search      | Perplexity         | Perplexity is designed for real-time search and can provide the most up-to-date information.          |
| Questions with citations  | Perplexity         | Perplexity provides sources for its answers, which is crucial for research and academic work.         |
| Deep research             | Perplexity         | Perplexity's ability to synthesize information from multiple sources makes it ideal for deep research. |
| Code generation           | OpenRouter         | OpenRouter offers access to specialized code generation models like Kimi K2 or DeepSeek.              |
| Creative writing          | OpenRouter         | OpenRouter provides a wide range of models suitable for creative tasks.                               |
| Product reviews           | OpenRouter         | OpenRouter models can generate fluent and coherent text for reviews.                                  |
