# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：[tool call]   glossary_search_glossary({'query': '3 levels'})
- STEP 3 の [tool call]：[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：[tool call]   aws_aws___search_documentation({'search_phrase': 'Amazon S3 versioning overview', 'topics': ['general']})
- 気づき・疑問：Using MCP (Model Context Protocol) allowed me to add external tools without modifying the agent's code. However, I noticed that as the number of available tools grows, the number of input tokens also increases due to the descriptions and argument definitions. I think it is important to have a mechanism that loads only the necessary tools.

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 
- やったこと：
- 結果：
- 気づき・疑問：

- 取り組んだレベル：実装 
- やったこと：
- 結果：
- 気づき・疑問：

- 取り組んだレベル：発展
- やったこと：
- 結果：
- 気づき・疑問：
