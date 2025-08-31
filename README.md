PythonChatBot/

│── README.md

│── requirements.txt

│── .env # keys + config

│── .gitignore

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

│ └── discord_bot/

│ └── bot.py

│── scripts/

│ └── test_cerebras.py

└── data/

├── chroma/ # vector DB persistence

├── uploads/ # ingested files

└── convos.db # sqlite for conversations


