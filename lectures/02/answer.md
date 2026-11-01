# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
- 自分で学習を実行したか（`executed_training_myself`）：はい / いいえ（実行できた範囲：　）
- 学習前：`format_rate` =　 / `content_rate` =　
- 学習後：`format_rate` =　 / `content_rate` =　
- 退行した質問：
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
- 学習で変わったこと・変わらなかったこと：

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
### 基礎：LoRAランクの比較: 
I have changed the `lora_r` from 16 to 8. Another settings was unchanged.

| 項目 | r=16 | r=8 |
| --- | ---: | ---: |
| 学習パラメータ数 | 6,389,760 | 3,194,880 |
| 最終 Training Loss（Step 40） | 0.014062 | 0.013375 |
| 学習時間 | 580 秒 | 376 秒 |
| format_rate（学習後） | 100% | 100% |
| content_rate（学習後） | 90.48% | 95.24% |

Reducing the `lora_r` value from 16 to 8 halved the number of trainable parameters and cut training time by approximately 35%. In both configurations, the model achieved 100% compliance with the required JSON format.
Although content accuracy improved from 90.48% to 95.24%, the evaluation was based on only 21 questions—meaning the difference amounts to just a single question. Consequently, it cannot be concluded that a rank of 8 is consistently superior to others.
Moreover, even with a rank of 8, there were instances where the system failed to identify the need for pre-registration confirmation—a point not covered in the FAQ.
These results suggest that while fine-tuning is effective for enforcing JSON formatting and response styles, it is difficult to entirely prevent the generation of unfounded or incorrect answers.

### 実装：医療情報管理システムのFAQによるLoRA学習: 

| 指標 | 学習前 | 学習後 |
| --- | ---: | ---: |
| format_rate | 19.05% | 100% |
| content_rate | 0% | 80.95% |
| both_rate | 0% | 80.95% |

Following the training, all 21 items were output in the correct JSON format. Furthermore, for the 6 questions that lacked supporting data in the FAQ, the system correctly identified all of them as requiring `needs_review=true`.
On the other hand, out of the 15 questions for which answers were available in the FAQ, 4 were incorrectly flagged as requiring further review.
The training process took 364 seconds, with a final recorded error of 0.014994.


- 変えた設定やデータ：
- 結果（比較表や数字）：
- ファインチューニングが向く場面・向かない場面についての考察：
