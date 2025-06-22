# South African Port Tariff Calculator (2024–2025)

This project provides an automated solution to calculate port tariffs for vessels arriving at South African ports (Durban, Saldanha, Richards Bay), based on the official tariff document for April 2024 – March 2025.

---

## 🧠 Approach

To ensure accurate and reliable results, the solution follows a structured, agent-based workflow:

### 1. Tariff Computation Functions

Each tariff component is implemented as a standalone Python function:

- Light dues  
- Port dues  
- Towage dues  
- Pilotage dues  
- VTS dues  
- Running of vessel lines dues  

### 2. User Input Understanding via Gemini

The vessel description is provided in natural language. A Gemini LLM is used to parse the input and extract structured vessel parameters such as:

- Port  
- GT / NT / DWT  
- LOA, Beam, Draft  
- Days Alongside  
- Cargo Quantity  
- Activity Type  

### 3. Agentic Orchestration

An intelligent planning agent (powered by Gemini) interprets the structured vessel data and determines:

- Which tariff functions to call  
- In what order  
- With which parameters  

This ensures dynamic and context-aware computation across ports and vessel types.

### 4. API with Swagger UI

The solution is exposed through a RESTful API using FastAPI. A Swagger interface is available for interactive testing.

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.10+  
- A virtual environment (recommended)  
- Access to the Gemini API (Google AI Studio or API key)  

### 📦 Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <project-folder>
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required dependencies**

```bash
pip install -r requirements.txt
```

## ▶️ Run the API Server

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs) to access Swagger UI and test the API interactively.
---


## 🔧 Tech Stack

- Python 3.10+  
- FastAPI  
- Gemini (Google Generative AI)  
- Uvicorn  
- Pydantic  
- Swagger/OpenAPI  
