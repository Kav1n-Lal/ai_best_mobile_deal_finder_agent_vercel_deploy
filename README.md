# 📱 Best Mobile Deal Finder Agent

An AI-powered conversational mobile deal finder built with **Python, LangGraph, FastAPI, PostgreSQL, Ollama, and Qwen3**.

The application helps users find and analyze mobile phone deals stored in a PostgreSQL database. It considers pricing, discounts, cashback, bank offers, exchange bonuses, delivery charges, availability, stock, warranty, and effective price.

The project also provides conversational memory using a LangGraph SQLite checkpointer and a web-based chatbot interface built with HTML, CSS, and JavaScript.

---

## ✨ Features

- 🤖 AI-powered mobile deal finder
- 🧠 LangGraph-based agent workflow
- 💬 Conversational chatbot interface
- 🧩 Qwen3 model through ChatOllama
- ⚡ FastAPI backend
- 🐘 PostgreSQL database integration
- 🔎 Mobile deal search and analysis
- 💰 Discount and effective price calculation
- 📦 Availability and stock information
- 🛡️ Warranty information
- 🧠 Persistent conversational memory using LangGraph SQLite checkpointing
- 🗑️ Clear current chat
- 📜 View chat history
- ❌ Delete chat history
- 📚 FastAPI Swagger API documentation
- 🧪 Pytest-based testing support

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| uv | Python package and environment management |
| FastAPI | Backend API |
| LangGraph | Agent workflow and orchestration |
| LangChain Core | LLM and agent abstractions |
| ChatOllama | Local LLM integration |
| Qwen3 | Large language model |
| PostgreSQL | Mobile deals database |
| SQLite | LangGraph conversational checkpoint memory |
| Pandas | Dummy data generation and processing |
| HTML | Chatbot interface |
| CSS | UI styling |
| JavaScript | Frontend interaction |
| Pytest | Testing |

---

## 🏗️ Project Architecture

```text
```

## 📂 Project Structure

```best_mobile_deal_finder_agent/
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
```
## 🗄️ Database
- The application uses PostgreSQL to store mobile deal information.

### Database
- mobile_deals

### Table
- **retailer_data** The retailer_data table contains information about mobile phones and their available deals.

## Mobile Pricing Data Schema

| Column | Type | Description |
| :--- | :--- | :--- |
| `retailer` | `str` | Retailer selling the mobile |
| `brand` | `str` | Mobile phone brand |
| `model` | `str` | Mobile phone model |
| `memory` | `str` | RAM/memory configuration |
| `storage` | `str` | Storage capacity |
| `mrp` | `float` | Maximum retail price |
| `selling_price` | `float` | Current selling price |
| `discount` | `float` | Discount amount |
| `cashback` | `float` | Cashback amount |
| `bank_offer` | `float` | Bank offer amount |
| `exchange_bonus` | `float` | Exchange bonus |
| `delivery_charge` | `float` | Delivery charge |
| `availability` | `bool` | Product availability |
| `stock_count` | `int` | Available stock |
| `warranty` | `str` | Warranty information |
| `effective_price` | `float` | Calculated effective price |
| `created_at` | `timestamp` | When was this data entered |

## 💰 Effective Price
- The application can use the following deal components to determine an effective price: 

```
Effective Price =
    Selling Price
    - Discount
    - Cashback
    - Bank Offer
    - Exchange Bonus
    + Delivery Charge
```
- The exact calculation is implemented by the application's service/deals.py file.

## 📋 Prerequisites
### Before running the project, install:

- Python 3.12

- uv

- PostgreSQL

- Ollama

- Qwen3

## 🚀 Installation
- Clone the Repository
```
git clone https://github.com/Kav1n-Lal/best_mobile_deal_finder_agent.git
```

```
cd best_mobile_deal_finder_agent
```


- Create the Python Environment
The project uses uv for dependency and virtual-environment management.

- Install the project dependencies:

```
uv venv
uv sync
```

## 🔐 Environment Variables
- Create a .env file in the project root.

```Example:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=mobile_deals
DB_USER=postgres
DB_PASSWORD=<your-password>
```
- Use the environment variable names required by your application's config.py.

## 🐘 PostgreSQL Setup
- Create the PostgreSQL database:

```
CREATE DATABASE mobile_deals;
```

- The application expects the mobile deal data to be stored in:

```
mobile_deals
     └── retailer_data
 ```

- The project includes a dummy data generator under:

```
src/best_mobile_deal_finder_agent/data_generator/
```
- The generator can be used to populate the database with development/demo data.

## 🤖 Ollama and Qwen3 Setup
- Install and start Ollama.

- Pull the Qwen3 model: ollama pull qwen3:8b

- Verify that the model is available:

- ollama list

- The application uses Qwen3 through ChatOllama.

- The default Ollama endpoint is:

- http://localhost:11434

## ▶️ Running the Application
- Start the FastAPI development server with:

```uv run uvicorn best_mobile_deal_finder_agent.main:app --reload```

- The application will be available at:

```http://127.0.0.1:8000```

- Open the application in your browser:

```http://127.0.0.1:8000```

## 📚 FastAPI Documentation
- FastAPI provides interactive API documentation.

- Swagger UI
```http://127.0.0.1:8000/docs```

- ReDoc
```http://127.0.0.1:8000/redoc```

## 💬 Chatbot Interface
### The project includes a web-based chatbot interface built using:

- HTML

- CSS

- JavaScript

### The user can interact with the mobile deals agent through the browser.

- The interface provides functionality for:

- Sending queries

- Receiving AI responses

- Maintaining conversation context

- Clearing the current chat

- Viewing chat history

- Deleting chat history

## 🔎 Example Queries

1. The chatbot can be used with queries such as:


- Show me Samsung mobile deals.

- Find phones under 30000.

- Compare available deals for Samsung and iPhone.


2. The results depend on the data available in the PostgreSQL retailer_data table.

## 🧠 Conversational Memory
- The application uses a LangGraph SQLite checkpointer for conversational memory.

- The local memory database is: **chat_memory.sqlite**

- This allows the application to maintain conversation state between messages.

- The SQLite memory database is intentionally excluded from Git version control.

- Each local installation can maintain its own conversation memory.

## 🧪 Dummy Data Generation
- The project contains a dummy mobile deal data generator:

```
src/best_mobile_deal_finder_agent/data_generator/
├── __init__.py
├── connection.py
└── generate_data.py
```

- After configuring PostgreSQL, run:

```
uv run python -m best_mobile_deal_finder_agent.data_generator.generate_data
```

- This can be used to generate development/demo data for the retailer_data table.

## 🛠️ Development Commands
- Install Dependencies
```
uv sync
```
- Add a Dependency
```
uv add <package-name>
```
- Remove a Dependency
```
uv remove <package-name>
```
- Update the Lock File
```
uv lock
```
- Run the Application
```
uv run uvicorn best_mobile_deal_finder_agent.main:app --reload
```
- Run Tests
```
uv run pytest
```

<!-- 
🧪 Testing
Tests are located in:

tests/
├── test_api.py
└── test_deals.py

Run the test suite with:

uv run pytest

For more detailed output:

uv run pytest -v -->
