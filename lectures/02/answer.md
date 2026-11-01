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
For a hypothetical medical information management system, a dataset in an FAQ format was prepared, covering five topics: system login, access rights, medical record storage, notifications, and error handling.
The dataset consisted of 14 training examples, 7 validation examples, and 21 test examples.
Following LoRA-based training, the adherence to the required format increased from 4.76% to 100%, while content accuracy improved from 4.76% to 85.71%. The training process took 232 seconds, resulting in a final loss value of approximately 0.0157.
Upon completion of training, the model generated responses in the correct JSON format for all test questions. However, in 3 out of 21 cases, the model produced content-related errors: for questions regarding editing rights for medical records, adding notification recipients, and 24/7 administrative support—topics not fully covered in the FAQ—the model incorrectly returned `needs_review: false`.
Additionally, the model was tested on 4 questions that were not part of the training set. It correctly identified that questions concerning data storage on overseas servers and biometric authentication required further review; however, it erred in responding to a question about the deletion of medical records (instead describing data storage methods). Conversely, the model provided correct answers to questions regarding physicians' rights to edit medical records—information that was included in the FAQ. This experiment demonstrates that, while the LoRA method is effective for mastering output data formats, challenges remain in determining the correct response when the data does not contain the information needed to answer the query.


- 変えた設定やデータ：
- 結果（比較表や数字）：
- ファインチューニングが向く場面・向かない場面についての考察：
