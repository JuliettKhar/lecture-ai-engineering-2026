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
- やったこと：Added get_lecture_summary to app/mcp_server.py and exposed it as an MCP tool without changing the agent code or configuration.
- 結果：The number of available tools increased from 7 to 8. The agent automatically discovered glossary_get_lecture_summary and successfully called it with {'lecture': 2}. All 21 tests passed.
- 気づき・疑問：I have confirmed that adding a tool on the MCP server side makes it automatically available to the agent. However, increasing the number of tools also leads to a rise in the number of input tokens consumed by their descriptions. I would like to explore the possibility of loading only those tools that are necessary for completing a specific task.

- 取り組んだレベル：実装 
- やったこと： Registered get_lecture_summary as an MCP tool. Then implemented make_quiz(lecture) in app/tools.py and exposed it through the MCP server. The new tool provides lecture content for generating review questions and returns a structured error for unavailable lecture numbers.
- 結果：The agent automatically discovered both new tools, increasing the total from 7 to 9. It successfully called glossary_get_lecture_summary({'lecture': 2}) and glossary_make_quiz({'lecture': 2}). For Lecture 99, the quiz tool returned lecture_not_found with the available lecture numbers [1, 2, 3, 4, 6], and the agent correctly explained the error to the user. All 21 tests passed.
- 気づき・疑問：MCP tools can be added without modifying the agent's implementation. Furthermore, I discovered that the successful discovery of a tool does not guarantee it will function correctly: a minor error in a file-searching pattern resulted in an empty list of available lectures. Identifying this issue was made possible by testing with both valid and invalid inputs. I am also interested in the possibility of reducing excessive token consumption by loading only those tool definitions that are actually required.

- 取り組んだレベル：発展
- やったこと：I reviewed the official documentation for Claude Code MCP and cross-referenced its provisions with the `app/mcp_servers.json` file, paying particular attention to configuration files, local and remote servers, and the scopes of configuration.
- 結果：Claude Code uses a `.mcp.json` file for project-level configuration, while `~/.claude.json` is used for local and user-level settings. For local servers, the `stdio` type is employed, requiring a `command` and `args`, whereas for remote servers, the `http` type is used, requiring a URL. Additionally, Claude Code supports three scopes: local, project, and user.
- 気づき・疑問：MCP provides a common protocol for connecting tools, but configuration details differ between clients. 
