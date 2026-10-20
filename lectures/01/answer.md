# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：I asked the model: "What are the three levels of homework assignments in the AIE2026 course?" The model provided a plausible description of the three levels of homework assignments; however, some details did not align with the actual definitions used in the course. The model did not have access to the course glossary when generating its response.
- 用語集の正しい意味と比べて気づいたこと： According to the file `data/glossary.json`, three levels are defined:
基礎 (Basic): Reviewing and internalizing lecture material.
実装 (Implementation): Writing and modifying program code.
発展 (Advanced): Exploration and experimentation.
Experiments have shown that when asked about facts related to a course that are not present in the provided context, an LLM may generate information that is convincing but incorrect. Supplying relevant source materials—such as a course glossary—helps improve the factual accuracy of the responses.
- 表示できたトークン数（入力 / 出力）： I modified app/ask.py to display token usage from the Gemini API's usage_metadata. Example using gemini-3.5-flash-lite and the prompt LoRAとは何ですか？:
Input tokens: 7
Output tokens: 597
Total tokens: 604

## 宿題

- 取り組んだレベル：発展 (Advanced); 基礎 (Basic) and 実装 (Implementation) were also completed.
- やったこと： I have added support for interactive chat—including conversation history—to the `app/ask.py` file. I also implemented the ability to select a model via command-line arguments and added tracking for response latency and token usage.
I compared several Gemini models using the same prompt—"What is LoRA?" (LoRAとは何ですか？)—by running three independent queries for each model with the `temperature` parameter set to 0.
Additionally, I examined thinking-token usage, API errors, and free-tier rate limits.
- 結果：

### モデル比較

The --chat option allows multiple messages within one session while preserving conversation history. In a test conversation, input token usage increased from 11 to 126 tokens as previous messages were included.

| Model                   | Runs | Average latency | Average output tokens | Average total tokens |
| ----------------------- | ---: | --------------: | --------------------: | -------------------: |
| `gemini-3.5-flash-lite` |    3 |         2.707 s |                 600.7 |                607.7 |
| `gemini-3.1-flash-lite` |    3 |         6.759 s |                 668.0 |                675.0 |
| `gemini-3.5-flash`      |    3 |        12.574 s |                 730.7 |               1664.7 |

The same input prompt, consisting of 7 tokens, was used for all requests. In this experiment, the gemini-3.5-flash-lite model demonstrated the lowest average latency.
An additional request to gemini-3.6-flash produced:
```text
[latency]: 10.989 s
[input tokens]: 7
[output tokens]: 674
[thoughts tokens]: 1006
[total tokens]: 1687
```

The total token count included thinking tokens, which were not part of the visible response. This explains why total token usage can be substantially larger than input and output tokens alone.

API errors and availability
Some requests to gemini-3.5-flash and gemini-3.6-flash returned HTTP 503 errors. A request to gemini-2.5-flash returned HTTP 404 because the model was unavailable to new users.
- 気づき・疑問：
Model latency and the number of tokens consumed can vary significantly, even when using the exact same prompt. Response times may also fluctuate across repeated requests to the same model.

Setting the `temperature` parameter to `0` does not always guarantee identical responses.

Tokens consumed during the "thinking" process can account for a substantial portion of the total token usage. If only the visible output tokens are considered, the actual consumption for models that employ a "thinking" mechanism will be understated.

API limits for the free tier vary depending on the specific model.

When conducting repeat experiments or automated evaluations, it is important to account for factors such as latency, total token consumption, request quotas, and retry strategies, rather than selecting a model based solely on the quality of its responses.
