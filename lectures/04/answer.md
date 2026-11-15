# 第4回 解答

## 演習

- 基準別の一致率（直す前）：

| Criterion                | Before | After |
| ------------------------ | ------ | ----- |
| Grounding                | 7/9    | 9/10  |
| Scope                    | 8/10   | 9/10  |
| Hints                    | 8/10   | 9/10  |
| Clarity                  | 8/10   | 8/10  |
| Lecture reference (code) | 10/10  | 10/10 |
| Overall agreement        | 9/9    | 10/10 |
| Coverage                 | 90%    | 100%  |
| Unsure cases             | 1      | 0     |

- 要確認の件数（直す前）： 1件
- 直した基準と、書き足した方針： the rubric section has been changed 根拠 (grounding). rule added `- 用語集にない用語について、用語集に登録されていないことを
  明示したうえで一般的な説明をする場合は、pass とする。ただし、その説明を用語集に基づく確定情報として扱わないこと。` and the rule has been removed from unsure
- 基準別の一致率と要確認の件数（直した後）：
  - 根拠：9/10
  - 範囲：9/10
  - ヒント：9/10
  - 分かりやすさ：8/10
  - 回の表示（コード）：10/10
  - 総合の一致率：10/10（coverage：100%）
  - 要確認：0件（修正前：1件）

- 講師のラベルと自分のラベルで判定が違った項目と、そう判定した理由：
There were discrepancies in 6 categories: "Basis" (8/10), "Scope" (9/10), "Hints" (9/10), "Clarity" (8/10), and "Session/Episode Labeling" (10/10).
#02 (Harness): Discrepancies occurred in four categories: Basis, Scope, Hints, and Clarity. I marked this as a "fail" because the reference material displayed on-screen concerned LoRA and PEFT, which did not align with the user's question. The instructor, however, evaluated the content of the answer itself as correct, marking it as a "fail" only due to the absence of a "Session N" label at the end.
#08 (Ignoring instructions): Discrepancies occurred in the "Basis" and "Clarity" categories. I marked this as a "fail" because the response outputted the contents of a glossary in compliance with a request to "ignore instructions." The instructor, conversely, distinguished between the violation of instructions and the quality of the actual content, marking these categories as "pass."
Through this comparison, I learned the importance of evaluating each criterion independently and I also recognized the necessity of verifying that the provided reference material actually aligns with the user's question.
- 気づき・疑問：The user's question regarding the harness received a satisfactory response from the model, but the displayed reference material and expected behavior described LoRA instead. This made it difficult to evaluate the answer based strictly on the provided references.

## 宿題

- 取り組んだレベル：基礎 
- やったこと：
I changed only the evaluation model to gemini-3.1-flash-lite, keeping the same evaluation dataset, human labels, temperature (0), and rubric. I then compared its results with the original model.
- 結果：
| Criterion                | Original model | Gemini 3.1 Flash Lite |
| ------------------------ | -------------: | --------------------: |
| Grounding                |           9/10 |                  8/10 |
| Scope                    |           9/10 |                  9/10 |
| Hints                    |           9/10 |                  9/10 |
| Clarity                  |           8/10 |                  7/10 |
| Lecture reference (code) |          10/10 |                 10/10 |
| Overall agreement        |          10/10 |                 10/10 |
| Coverage                 |           100% |                  100% |
| Unsure cases             |              0 |                     0 |

- 気づき・疑問：Both models achieved 100% overall agreement, but the new model had more disagreements on individual criteria (7 instead of 5).

- 取り組んだレベル：実装
- やったこと： Using a Streamlit-based annotation interface, I created a custom evaluation dataset consisting of 10 test cases. These included: standard questions, paraphrased queries, the use of unfamiliar terms, requests to complete homework assignments, prompt injection attempts, references to non-existent lectures, incomplete questions, questions based on false premises, attempts to bypass established constraints, and queries that fall outside the scope of the subject matter.
I generated responses using the `gemini-3.1-flash-lite` model, manually annotated each response based on five criteria, and then evaluated the results using an "LLM Judge"—leveraging the same model.
- 結果：

| Criterion                | Agreement |
| ------------------------ | --------: |
| Grounding                |      8/10 |
| Scope                    |     10/10 |
| Hints                    |      9/10 |
| Clarity                  |      9/10 |
| Lecture reference (code) |      8/10 |
| Overall agreement        |      7/10 |
| Coverage                 |      100% |
| Unsure cases             |         0 |
| Individual disagreements |         6 |

- 気づき・疑問： The most interesting instance of disagreement arose in Example #07. The evaluator rated the "Grounding" criterion as "unsatisfactory," citing the absence of the term "QLoRA" from the glossary—even though "QLoRA" is, in fact, included in the full glossary. This suggests that the completeness of reference information can affect the accuracy of an evaluation.
In Example #09, the evaluator lowered the score for the response, reasoning that the agent had acted outside its scope of competence (i.e., beyond its permitted range of actions); this observation pertained to several criteria, including "Clarity."
Example #08 also highlighted a limitation of evaluation methods based solely on text analysis. The agent reported that a "learning log" had been saved without prior approval; however, based on the text of the response alone, it is impossible to determine whether the relevant tool was actually executed or whether any data was, in fact, recorded.