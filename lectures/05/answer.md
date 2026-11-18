# 第5回 解答

## 演習

- 回答モデル（実行時の`[model]`）： google:gemini-3.5-flash-lite
- 比較した質問：In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add?
- 対象資料（全文投入と他の方式で範囲が違う点も記録）：data/rag_data/lectures.json. Full Context covers 9 documents (438 pages), while Vector Search, Tree, and Graph cover the main materials from Lectures 1–3 (214 pages). 

### 各方式の結果

| 方式 | 回答の要点・正しさ | 引用ページと根拠 | 時間（秒） | 入力／出力トークン数 | モデル応答回数 | 生成API推定費用（USD） |
|---|---|---|---|---|---|---|
| 全文投入 | Correct. LoRA freezes the original weights and trains low-rank matrices A and B. QLoRA adds 4-bit quantization. | Lecture 2, pp. 51–52. The explanation matches the materials. | 5.61 | 117,023 / 150 | 1 | $0.035482 |
| ベクトル検索 | Correct. Explained the same concepts accurately. | Lecture 2, pp. 51–52. Both pages provide supporting evidence. | 5.28 | 3,025 / 196 | 2 | $0.001398 |
| Tree | Correct. Also explained the memory-saving benefit of QLoRA. | Lecture 2, pp. 51–52. Retrieved the full text of both pages. | 17.02 | 13,694 / 375 | 6 | $0.005046 |
| Graph | Correct. Explained LoRA's trainable matrices and QLoRA's 4-bit quantization. | Lecture 2, pp. 51–52. The cited information supports the answer. | | | | |

<!-- 未実行・算定不可の場合は、その旨を書いてください。質問を追加した場合は、質問ごとに表を分けてください。 -->

- 検索だけを実行して見つかったページと、その本文で確認できたこと：uv run python -m app.retrieval "LoRA QLoRA difference"
- `--trace`で見えたツール呼び出し（ツール名・引数・回数、Treeでたどった目次など）： 
Full context: no tool calls; 1 model response.
Vector search: one call to `search_materials({'query': 'LoRA freeze train QLoRA add'})`; 2 model responses.
Tree: five calls to `browse_tree` following this path: root → lec02-main → lec02-main-s045 → lec02-main-p051 → lec02-main-p052. The agent retrieved the full text of pages 51 and 52; 6 model responses.
Graph: one call to `search_graph({'query': 'LoRA freeze train QLoRA'})`; 2 model responses. Page 52 appeared among the initial search results (source nodes).
- 取得した情報が足りなかった例、取得できたのに回答へ使えなかった例：No such failure was observed for this question
- 今回の用途に採用したい方式と、その理由・比較条件の限界：All four methods answered correctly, but Vector Search used the fewest input tokens and had the lowest estimated generation cost.
- 気づき・疑問：

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと（変更したファイル・設定・処理、または設計した取得方法）：Changed RAG_TOP_K from 5 to 2 in app/config.py to reduce the number of retrieved pages passed to the model.
- 比較した質問と、固定した条件（モデル・対象資料など）：Question: In Lecture 2, what does LoRA freeze and what does it train? What does QLoRA add? Model: google:gemini-3.5-flash-lite. Materials: Main lecture documents from Lectures 1–3 (214 pages), using the existing vector search index.
- 結果（変更前後の回答・根拠、`--trace`の出力、時間・トークン数・生成API推定費用など）：Both before and after the changes, the agent correctly explained that the LoRA method freezes the weights of the original model, training only the low-rank matrices A and B, while QLoRA additionally employs 4-bit quantization. In both instances, the execution logs (trace) show a single call to the `search_materials` function with the search query "LoRA freeze train QLoRA add."
Reducing the Top-K parameter from 5 to 2 resulted in a decrease in the number of input tokens by approximately 42.6% and a reduction in the estimated generation cost by 25.9%, with no loss in the accuracy of the responses in this test.

| Metric | Before (Top-5) | After (Top-2) |
|---|---:|---:|
| Answer correctness | Correct | Correct |
| Cited evidence | Lecture 2, pp. 51–52 | Lecture 2, pp. 51–52 |
| Tool calls | 1 `search_materials` | 1 `search_materials` |
| Model responses | 2 | 2 |
| Time | 5.28 s | 4.04 s |
| Input tokens | 3,025 | 1,736 |
| Output tokens | 196 | 206 |
| Estimated generation API cost | $0.001398 | $0.001036 |

- 改善した例と、残る失敗・制約：The improvement worked for this question because the two highest-ranked pages (Lecture 2, pp. 52 and 51) already contained sufficient evidence.
- 気づき・疑問：Retrieving more pages does not always improve an answer. In this case, a smaller context was sufficient and reduced token usage and cost.


- 取り組んだレベル：実装
- やったこと（変更したファイル・設定・処理、または設計した取得方法）：I added the `search_with_adjacent_pages()` function to `app/retrieval.py`. After performing a vector search, it includes the page immediately preceding and the page immediately following each retrieved page, while using the document identifier to ensure the search does not go beyond the document's boundaries. In `app/tools.py`, I introduced an environment variable, `RAG_INCLUDE_ADJACENT`, which allows for toggling between the standard vector search and this extended version without requiring any modifications to the original `search()` function.
- 比較した質問と、固定した条件（モデル・対象資料など）：Q1: What does LoRA freeze and train? What does QLoRA add?
Q2: What is the difference between compaction and cross-session memory? Do all daily notes become long-term memory?
Model: gemini-3.5-flash-lite
Materials: Lecture 1–3 main documents (214 pages).
Both modes used RAG_TOP_K = 2, the same model, materials, and agent instructions.
- 結果（変更前後の回答・根拠、`--trace`の出力、時間・トークン数・生成API推定費用など）：

**Results**

| Question | Mode | Answer | Evidence | Time (s) | Input / output tokens | Model calls | Est. cost |
|---|---|---|---|---:|---:|---:|---:|
| Q1 LoRA / QLoRA | Basic RAG | Correct | Lecture 2, pp. 51–52 | 3.47 | 1,736 / 192 | 2 | $0.001001 |
| Q1 LoRA / QLoRA | Adjacent | Correct | Lecture 2, p. 52 | 3.19 | 2,434 / 176 | 2 | $0.001170 |
| Q2 Compaction / Memory | Basic RAG | Correct | Lecture 3, pp. 38, 40, 65 | 6.75 | 3,401 / 386 | 3 | $0.001985 |
| Q2 Compaction / Memory | Adjacent | Correct | Lecture 3, pp. 38–40, 65 | 13.57 | 7,393 / 562 | 3 | $0.003623 |

For query Q1, both modes called the `search_materials` function once. The standard search (Top-2) returned pages 52 and 51. Expanding the search scope to adjacent pages added pages 53 and 50; no duplicates were generated in the process. For query Q2, both modes called `search_materials` twice. The first search yielded pages 65 and 39 from Lecture 3. Expanding the search scope to adjacent pages allowed for the inclusion of nearby pages—specifically page 38 and, potentially, page 40. The second search successfully located page 40, enabling both modes to provide the correct answer to the question regarding daily notes.
- 改善した例と、残る失敗・制約：Expanding the context to include adjacent pages successfully increased the scope of supporting evidence, while avoiding data duplication and ensuring the information remained within the document's boundaries.
However, no improvement in answer accuracy was observed in any of the tests. For the first question (Q1), the number of input tokens increased by approximately 40%. For the second question (Q2), the volume of input tokens grew by about 117%, and the estimated generation costs rose by approximately 83%.
- 気づき・疑問：n these tests, Basic RAG was sufficient, and the additional pages increased token usage and cost.
