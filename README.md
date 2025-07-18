# 🧠 Agentic AI-Based Conversational Website Editor with Toolformer-style Agents

## 🎯 Objective

To build an **agentic AI system** that allows users to **edit websites by using natural language commands**. where each user instruction is interpreted and directed to the appropriate editing agent, ensuring modular and explainable updates.

---

## 📌 Project Scope

- Accept user input in **natural language** to modify website structure, style, or content.
- Use **multi-agent architecture** to:
  - Parse commands
  - Route them to the correct tool
  - Apply the changes
  - Manage edit history
- Enable **real-time updates** to editable blocks (HTML/CSS/JS) within a browser interface.
- Support **undo** actions.
- Maintain **context-awareness** across sessions.
- Incorporate **RAG** (Retrieval-Augmented Generation) to provide policy-compliant feedback or clarify ambiguous instructions.

---
## 🔁 Agentic AI Workflow – Architecture Diagram
![diagram-export-6-20-2025-7_20_28-PM   ihub agent](https://github.com/user-attachments/assets/8372a1cc-c811-4c96-9c72-91fc3487146c)

## 🔁 Agentic AI Workflow – Demo video
https://drive.google.com/file/d/1Km2BCSOtB0Z7VfoBLu1i4SbaKbn6LXeu/view?usp=sharing

## 🗃️ System Architecture Components

### 🖥️ Client
- **Editor UI** (next.js-based)
- Accepts user input and displays real-time changes

### ⚡ FastAPI Server
- Routes and processes requests between UI and agents

### 🧠 Agentic AI (Python backend)
- NL Parser Agent
- Tool Router Agent (RAG-enabled)
- Change Executor Agent
- Undo Manager

### 📚 Data Storage
- **Knowledge Store** (for RAG lookups and policy)
- **Session Store** (for edit history and context)

---

## 📌 How It Works (Summary Flow)

1. User types a natural language command in the UI.
2. FastAPI sends it to **NL Parser Agent**.
3. **Tool Router Agent** (with RAG) chooses the right tool.
4. **Change Executor Agent** applies the changes to the site.
5. **Undo Manager** logs changes and allows reversal.
6. Changes are shown live and session state is saved.

---

## 🛠 Tech Stack

- **Frontend**: Next.js, Typescript, Tailwind CSS
- **Backend**: Python (FastAPI)
- **Agents**: Toolformer-style modular AI agents
- **Storage**: In-memory for RAG

---

## 🧪 Future Enhancements

- Multi-user collaboration
- Voice command integration
- Plugin support for custom tools

---
## TO Run the application 
```bash
git clone https://github.com/naveenmvoff/Agentic-AI-Workshop.git
```
### client 

```bash
cd Day10-FinalHackathon/aiconversationalweb

npm i

npm run dev

open the url and access the client side
```

### server

```
cd Day10-FinalHackathon/python-backend-for-ai

pip install -r requirements.txt

python main.py
```



© 2025 – Agentic AI Workshop Final Hackathon
