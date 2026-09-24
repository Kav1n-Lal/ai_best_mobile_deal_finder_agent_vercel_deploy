Best Mobile Deal Finder Agent

An AI-powered mobile deals finder agent built with Python, LangGraph, FastAPI, PostgreSQL, ChatOllama, and Qwen3.

The application provides a conversational chatbot that helps users find and analyze mobile phone deals stored in a PostgreSQL database. It considers pricing, discounts, cashback, bank offers, exchange bonuses, delivery charges, availability, stock, warranty, and effective price.

The project also provides conversational memory using a LangGraph SQLite checkpointer and a web-based chatbot interface built with HTML, CSS, and JavaScript.

Features

🤖 AI-powered mobile deal finder

🧠 LangGraph-based agent workflow

💬 Conversational chatbot interface

🧩 Qwen3 model through ChatOllama

⚡ FastAPI backend

🐘 PostgreSQL database integration

🔎 Mobile deal search and analysis

💰 Discount and effective price calculation

💳 Cashback and bank-offer analysis

🔄 Exchange bonus analysis

📦 Availability and stock information

🛡️ Warranty information

🧠 Persistent conversational memory using LangGraph SQLite checkpointing

🗑️ Clear current chat

📜 View chat history

❌ Delete chat history

📚 FastAPI Swagger API documentation

🧪 Pytest-based testing support

Tech Stack
Technology	Purpose
Python 3.12	Application development
uv	Python package and environment management
FastAPI	Backend API
LangGraph	Agent workflow and orchestration
LangChain Core	LLM and agent abstractions
ChatOllama	Local LLM integration
Qwen3	Large language model
PostgreSQL	Mobile deals database
SQLite	LangGraph conversational checkpoint memory
Pandas	Dummy data generation and processing
Selenium	Web automation
HTML	Chatbot interface
CSS	UI styling
JavaScript	Frontend interaction
Pytest	Testing
Project Architecture
                         ┌───────────────────────┐
                         │       Chatbot UI      │
                         │     HTML / CSS / JS   │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │        FastAPI        │
                         │        main.py        │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │       LangGraph       │
                         │        graph.py       │
                         └───────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
             ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
             │ Mobile Info │  │   Summary   │  │   Mobile    │
             │    Agent    │  │    Agent    │  │    Tools    │
             └─────────────┘  └─────────────┘  └──────┬──────┘
                                                       │
                                                       ▼
                                             ┌──────────────────┐
                                             │    PostgreSQL    │
                                             │   mobile_deals   │
                                             │  retailer_data   │
                                             └──────────────────┘

                         ┌───────────────────────┐
                         │  LangGraph SQLite     │
                         │      Checkpointer     │
                         │   chat_memory.sqlite  │
                         └───────────────────────┘

Project Structure
best_mobile_deal_finder_agent/
│
├── src/
│   └── best_mobile_deal_finder_agent/
│       ├── __init__.py
│       ├── config.py
│       ├── db.py
│       ├── graph.py
│       ├── llm.py
│       ├── main.py
│       ├── memory.py
│       ├── models.py
│       ├── mobile_info_agent.py
│       ├── summary_agent.py
│       │
│       ├── data_generator/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   └── generate_data.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   └── deals.py
│       │
│       └── tools/
│           ├── __init__.py
│           └── mobile_tools.py
│
├── static/
│   ├── css/
│   │   └── chat.css
│   └── js/
│       └── chat.js
│
├── templates/
│   ├── chat.html
│   └── index.html
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_deals.py
│
├── .env.example
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock

Database

The application uses PostgreSQL to store mobile deal information.

Database
mobile_deals

Table
retailer_data


The retailer_data table contains information about mobile phones and their available deals.

Data Fields
Column	Type	Description
retailer	str	Retailer selling the mobile
brand	str	Mobile phone brand
model	str	Mobile phone model
memory	str	RAM/memory configuration
storage	str	Storage capacity
mrp	float	Maximum retail price
selling_price	float	Current selling price
discount	float	Discount amount
cashback	float	Cashback amount
bank_offer	float	Bank offer amount
exchange_bonus	float	Exchange bonus
delivery_charge	float	Delivery charge
availability	bool	Product availability
stock_count	int	Available stock
warranty	str	Warranty information
effective_price	float	Calculated effective price
Effective Price

The application can use deal components such as:

Selling Price
- Discount
- Cashback
- Bank Offer
- Exchange Bonus
+ Delivery Charge


to determine an effective price for comparing mobile deals.

The exact calculation is implemented by the application's deal service/tooling layer.

Prerequisites

Before running the project, install:

Python 3.12

uv

PostgreSQL

Ollama

Qwen3

Installation
1. Clone the Repository
git clone https://github.com/<YOUR_USERNAME>/best_mobile_deal_finder_agent.git
cd best_mobile_deal_finder_agent

2. Create the Python Environment

The project uses uv for dependency and virtual-environment management.

Install the project dependencies:

uv sync


uv will create the project's .venv environment and install the dependencies specified in pyproject.toml.

Environment Variables

Create a .env file in the project root.

Example:

DATABASE_URL=postgresql://username:password@localhost:5432/mobile_deals
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen3


Use the environment variable names required by your application's config.py.

A .env.example file is included in the repository as a template.

Important: Never commit your .env file or database passwords to GitHub.

PostgreSQL Setup

Create the PostgreSQL database:

CREATE DATABASE mobile_deals;


The application expects the mobile deal data to be stored in:

mobile_deals
└── retailer_data


The project includes a dummy data generator under:

src/best_mobile_deal_finder_agent/data_generator/


The generator can be used to populate the database with development/demo data.

Ollama and Qwen3 Setup

Install and start Ollama.

Pull the Qwen3 model:

ollama pull qwen3


Verify that the model is available:

ollama list


The application uses Qwen3 through ChatOllama.

The default Ollama endpoint is:

http://localhost:11434

Running the Application

Start the FastAPI development server with:

uv run uvicorn best_mobile_deal_finder_agent.main:app --reload


The application will be available at:

http://127.0.0.1:8000


Open the application in your browser:

http://127.0.0.1:8000

FastAPI Documentation

FastAPI provides interactive API documentation.

Swagger UI
http://127.0.0.1:8000/docs

ReDoc
http://127.0.0.1:8000/redoc

Chatbot Interface

The project includes a web-based chatbot interface built using:

HTML

CSS

JavaScript

The user can interact with the mobile deals agent through the browser.

The interface provides functionality for:

Sending messages

Receiving AI responses

Maintaining conversation context

Clearing the current chat

Viewing chat history

Deleting chat history

Example Queries

The chatbot can be used with queries such as:

Find the cheapest mobile available.

Show me Samsung mobile deals.

Find phones under 30000.

Which mobile has the lowest effective price?

Compare available deals for Samsung and iPhone.

Which phones have cashback?

Show me mobiles with bank offers.

Find mobiles with exchange bonuses.

Show available phones with the highest discount.


The results depend on the data available in the PostgreSQL retailer_data table.

Conversational Memory

The application uses a LangGraph SQLite checkpointer for conversational memory.

The local memory database is:

chat_memory.sqlite


This allows the application to maintain conversation state between messages.

The SQLite memory database is intentionally excluded from Git version control.

Each local installation can maintain its own conversation memory.

Dummy Data Generation

The project contains a dummy mobile deal data generator:

src/best_mobile_deal_finder_agent/data_generator/
├── __init__.py
├── connection.py
└── generate_data.py


After configuring PostgreSQL, run:

uv run python -m best_mobile_deal_finder_agent.data_generator.generate_data


This can be used to generate development/demo data for the retailer_data table.

Development Commands
Install dependencies
uv sync

Add a dependency
uv add <package-name>

Remove a dependency
uv remove <package-name>

Update the lock file
uv lock

Run the application
uv run uvicorn best_mobile_deal_finder_agent.main:app --reload

Run tests
uv run pytest

Run a Python module
uv run python -m best_mobile_deal_finder_agent.<module>

Testing

Tests are located in:

tests/
├── test_api.py
└── test_deals.py


Run the test suite with:

uv run pytest


For more detailed output:

uv run pytest -v

GitHub Setup

Initialize Git in the project directory:

git init


Check the repository status:

git status


Add the project files:

git add .


Create the initial commit:

git commit -m "Initial commit - Best Mobile Deal Finder Agent"


Rename the default branch to main:

git branch -M main


Add your GitHub repository:

git remote add origin https://github.com/<YOUR_USERNAME>/best_mobile_deal_finder_agent.git


Push the project:

git push -u origin main

Important Files
File	Purpose
pyproject.toml	Project metadata and dependencies
uv.lock	Locked dependency versions
.python-version	Python version used by uv
.env.example	Environment variable template
.gitignore	Files excluded from Git
main.py	FastAPI application
graph.py	LangGraph workflow
llm.py	LLM configuration
memory.py	Conversation memory/checkpointer
db.py	Database configuration/connection
models.py	Data models
mobile_info_agent.py	Mobile information agent
summary_agent.py	Summary/response agent
services/deals.py	Mobile deal service logic
tools/mobile_tools.py	Tools used by the agent
Security

Do not commit sensitive information to the repository.

The following should remain local:

.env
.venv/
chat_memory.sqlite
*.sqlite
*.sqlite3


Never hard-code:

PostgreSQL passwords

API keys

Access tokens

Authentication credentials

Private connection strings

Use environment variables instead.

Disclaimer

This project currently uses dummy mobile deal data for development and demonstration purposes.

Prices, discounts, cashback, bank offers, exchange bonuses, delivery charges, stock counts, availability, warranty information, and effective prices should not be considered real-time retailer information unless the application is connected to a live data source.

Author

Kav1n-Lal

GitHub: https://github.com/<YOUR_USERNAME>

License

This project does not currently specify a license.

If you intend to make the project open source, add an appropriate LICENSE file to the repository.