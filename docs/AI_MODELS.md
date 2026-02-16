# AI Models and Ecosystem Documentation

This document provides a comprehensive overview of the AI models and the underlying strategy for their use across this project. Our approach is designed to be cost-effective, efficient, and adaptable, prioritizing open-source and free models while escalating to premium models only when necessary.

## Overall AI Model Strategy

The core of our AI strategy is a "Free-First" or "FOSS-First" approach. We begin with free or low-cost models and only escalate to more powerful, premium models when the task complexity demands it. This is managed through an automated routing system that optimizes for cost and performance, tracks usage per model, and automatically hands off to the next tier if a model is rate-limited or otherwise unavailable.

## Multi-Model Brainstorming Session

A multi-model brainstorming session was conducted using OpenRouter to generate a wide range of ideas and perspectives. This session involved eight different models, incurring a total cost of $0.12 for 52,675 tokens.

| Model Name                  | Provider      | Purpose in Brainstorming                                  | Strengths                                       | Cost Tier |
| --------------------------- | ------------- | --------------------------------------------------------- | ----------------------------------------------- | --------- |
| DeepSeek V3                 | deepseek      | General brainstorming and idea generation                 | Strong general capabilities                     | Budget    |
| Google Gemini 2.0 Flash     | google        | Quick and efficient idea generation                       | High speed and low latency                      | Budget    |
| Anthropic Claude 3.5 Haiku  | anthropic     | Creative and nuanced brainstorming                        | Strong language understanding and generation    | Mid       |
| Meta Llama 3.3 70B          | meta-llama    | In-depth and complex idea exploration                     | Large parameter count for deep reasoning        | Mid       |
| Mistral Small 3.1 24B       | mistralai     | Efficient and cost-effective brainstorming              | Good balance of performance and cost            | Budget    |
| Qwen 2.5 72B                | qwen          | Broad and diverse idea generation                         | Large context window and strong multilingual support | Mid       |
| Microsoft Phi-4             | microsoft     | Compact and efficient brainstorming                       | High performance for its size                   | Budget    |
| NVIDIA Nemotron Ultra 253B  | nvidia        | High-end, frontier-level brainstorming for complex problems | Massive parameter count for cutting-edge performance | Premium   |

## Model Routing and Selection Strategy

Our soul/preferences are configured with a sophisticated model routing strategy to ensure the best model is used for each specific task. This allows for a balance of cost, speed, and capability.

### Free-First Stack

This is the default stack, designed to handle most tasks with free or very low-cost models.

1.  **MiMo-V2-Flash:** The first choice for its speed and efficiency.
2.  **Trinity-Large-Preview:** A powerful free-tier model.
3.  **Venice Uncensored:** Used for tasks requiring a less restrictive model.
4.  **Llama 3.3 70B:** A high-performing free-tier model for more complex tasks.
5.  **DeepSeek V3.2:** The final fallback in the free tier, offering a good balance of cost and performance.

Premium models are only engaged when the free-tier models are insufficient for the task at hand.

### Task-Specific Model Preferences

| Task Category         | Primary Model(s)                                       | Rationale                                                              | Cost Tier(s)       |
| --------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------- | ------------------ |
| **Code Generation**   | Kimi K2.5 (moonshotai/kimi-k2)                           | Excellent for generating high-quality, coherent code.                  | Mid                |
| **Code Review**       | Venice AI → DeepSeek V3.2 Speciale or Claude Sonnet 4.5 | Venice AI provides specialized code review, with strong fallbacks.      | Mid / Premium      |
| **Cost-Effective**    | DeepSeek V3.2                                          | Offers performance at 1/100th of the cost of frontier models.          | Budget             |
| **Fast Iteration**    | Grok Code Fast 1                                       | Extremely fast token generation (190 tok/sec) for rapid development.   | Budget             |
| **Complex Reasoning** | Gemini 2.5 Pro                                         | Ranked #1 on the LMSYS Chatbot Arena for complex reasoning tasks.      | Premium            |
| **Agentic Tasks**     | Grok 4.1 Fast or Claude Sonnet 4.5                     | Well-suited for autonomous, multi-step tasks.                          | Mid / Premium      |
| **Free Tier**         | Trinity-Large-Preview, Llama 3.3 70B, gpt-oss-120b       | A selection of powerful models available at no cost.                   | Free               |
