PythonChatBot/

│── README.md

│── requirements.txt

│── .env # keys + config

│── .gitignore

├── cli/

│ ├── __init__.py

│ ├── commands.py

│ ├── completers.py

│ ├── main.py

│ └── utils.py

│── src/

│ ├── config.py

│ ├── llm/

│ │ ├── base.py

│ │ └── cerebras.py

│ ├── memory/

│ │ ├── convo_store.py

│ │ ├── kb_store.py

│ │ └── chunking.py

│ ├── tools/

│ │ ├── web.py

│ │ ├── ingest.py

│ │ └── code_index.py

│ ├── core/

│ │ ├── prompts.py

│ │ └── chatbot.py

│ ├── webapp/

│ │ └── app.py

│ ├── discord_bot/

│ │ └── bot.py

│── scripts/

│ ├── clear_active_history.py

│ ├── dump_archive.py

│ ├── list_users.py

│ ├── list_workspaces.py

│ ├── merge_archive_active.py

│ ├── view_conversation.py

│ ├── test_cerebras.py

│ ├── README.md

│ └── CONTRIBUTING.md

└── data/

├── chroma/ # vector DB persistence

├── uploads/ # ingested files

└── convos.db # sqlite for conversations



