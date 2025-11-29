
# Enterprise Support Automator (ESA) - Capstone Project

**Track:** Enterprise Agents  
**Project:** Enterprise Support Automator (ESA)  



## 🎯 Problem Statement

### The Challenge
Modern enterprises face significant operational challenges in customer support:

- **Scalability**: Manual support teams cannot scale to handle high-volume customer inquiries
- **24/7 Availability**: Round-the-clock support is expensive and resource-intensive
- **Consistency**: Different agents provide varying quality of service and information
- **Speed**: Customers wait long periods for responses, leading to poor satisfaction
- **Complex Workflows**: Support scenarios often require approval workflows and multi-step reasoning
- **Context Awareness**: Support agents need access to multiple data sources (product catalog, order history, etc.)

### Business Impact
- Customer dissatisfaction due to response delays
- Operational costs from large support teams
- Missed sales opportunities during peak demand
- Inability to handle complex multi-step requests (e.g., refund approvals)

---

## ✨ Solution Overview

**Enterprise Support Automator (ESA)** is an AI-powered customer support platform built on **Google's Agent Development Kit (ADK)** that:

1. **Automates Support Workflows**: Uses intelligent agents to handle customer inquiries with natural language understanding
2. **Multi-Agent Architecture**: Specialized agents for different domains (product info, order lookup, refunds)
3. **Approval Workflows**: Implements human-in-the-loop for sensitive operations (large refunds, escalations)
4. **Session Persistence**: Maintains conversation context across interactions using resumable sessions
5. **Real-time Chat Interface**: User-friendly React frontend for seamless customer interactions
6. **Observable & Evaluable**: Comprehensive logging, event tracking, and test suite for validation

### Key Benefits
✅ **Reduce Support Costs**: Automate 80%+ of routine inquiries  
✅ **Improve Response Time**: Instant replies 24/7  
✅ **Maintain Quality**: Consistent, accurate information from structured tools  
✅ **Enable Scalability**: Handle unlimited concurrent support sessions  
✅ **Risk Mitigation**: Human approval for high-value operations  

---

## 🏗️ Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client Layer                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │   React + Vite Frontend (Chat UI)                            │  │
│  │   - Real-time message display                               │  │
│  │   - Session management (localStorage)                       │  │
│  │   - Approval UI (pending items)                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────────────┐
│                      Backend Layer (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  /message - POST (send user message)                         │  │
│  │  /approve - POST (submit approval response)                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↕                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │      Google ADK Runner & Session Service                     │  │
│  │  - Event processing & orchestration                          │  │
│  │  - Session state management                                  │  │
│  │  - Tool invocation & context passing                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    Agent & Tool Layer (ADK)                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Support App (Resumable)                                     │  │
│  │  └─ Root Agent: customer_support_agent                       │  │
│  │     ├─ Tool: AgentTool(product_catalog_agent)              │  │
│  │     ├─ Tool: order_lookup()                                 │  │
│  │     └─ Tool: request_refund() [with approval flow]         │  │
│  │        └─ Sub-agent: product_catalog_agent                 │  │
│  │           └─ Tool: product_catalog_lookup()                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                          ↕                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │     Gemini 2.5 Flash Lite LLM (Google)                       │  │
│  │  - Natural language understanding & generation               │  │
│  │  - Multi-step reasoning & planning                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────────┐
│                      Data & External Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  SQLite DB   │  │  Product DB  │  │  Order DB    │              │
│  │  (Sessions)  │  │  (Mocked)    │  │  (Mocked)    │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Interaction Flow

```
User Message
    ↓
┌─────────────────────────────────────┐
│  customer_support_agent             │
│  (Gemini LLM)                       │
│  - Understands user intent          │
│  - Routes to appropriate tool       │
└─────────────────────────────────────┘
    ↓
    ├─→ Need Product Info? → product_catalog_agent → product_catalog_lookup()
    │
    ├─→ Need Order Info? → order_lookup()
    │
    └─→ Need Refund? → request_refund()
           ↓
           Is amount ≤ $100?
           ├─→ YES: Auto-approve
           └─→ NO: Request Human Approval
              ↓
              Tool Context → adk_request_confirmation
              ↓
              User Response (via /approve endpoint)
              ↓
              Continue Processing
    ↓
Response to User
```

### Data Flow Diagram

```
┌───────────────┐
│  User Input   │
│   (Chat UI)   │
└───────┬───────┘
        │ HTTP POST /message
        ↓
┌──────────────────────────┐
│  FastAPI Endpoint        │
│  - Extract session_id    │
│  - Create/Get session    │
│  - Wrap user message     │
└──────────┬───────────────┘
           │
           ↓
┌──────────────────────────┐
│  ADK Runner              │
│  - Async message handler │
│  - Event emission        │
└──────────┬───────────────┘
           │
           ├─────────────────────────────────────────┐
           ↓                                         ↓
    ┌───────────────┐                      ┌──────────────────┐
    │ Agent Logic   │                      │ Tool Execution   │
    │ (LLM Call)    │                      │ (Data Access)    │
    └───────────────┘                      └──────────────────┘
           │                                         │
           └─────────────────────────────────────────┘
                          ↓
                   ┌──────────────┐
                   │ Event Stream │
                   └──────┬───────┘
                          │
                          ├─→ Text Responses
                          ├─→ Approval Requests
                          └─→ Function Calls
                          ↓
                   ┌──────────────┐
                   │  HTTP Reply  │
                   │  (Frontend)  │
                   └──────────────┘
```

---

## 🔧 System Components

### Backend Components

#### 1. **FastAPI Server** (`backend/main.py`)
- REST API endpoints for messaging and approvals
- CORS middleware for cross-origin requests
- Session management with SQLite
- Event-based async message processing

**Key Endpoints:**
- `POST /message`: Send user message and get agent responses
- `POST /approve`: Submit approval decision for pending requests

#### 2. **ADK Agents** (`backend/agents.py`)
Implements a hierarchical agent structure:

| Agent | Purpose | Tools | Model |
|-------|---------|-------|-------|
| **customer_support_agent** | Main entry point; routes requests | product_catalog_agent, order_lookup, request_refund | Gemini 2.5 Flash Lite |
| **product_catalog_agent** | Product information lookups | product_catalog_lookup | Gemini 2.5 Flash Lite |

#### 3. **Tools**
- **`product_catalog_lookup(product_name)`**: Returns product info from catalog
- **`order_lookup(order_id)`**: Retrieves order status and details
- **`request_refund(order_id, amount, tool_context)`**: Processes refunds with optional approval

#### 4. **Session Service**
- SQLAlchemy-based DatabaseSessionService
- Persistent conversation state
- Support for resumable workflows
- SQLite backend (configurable)

### Frontend Components

#### 1. **Chat Interface** (`frontend/src/pages/Chat.jsx`)
- Real-time message display
- Session persistence (localStorage)
- Typing indicators
- Error handling

#### 2. **Styling** (`frontend/src/pages/chat.css`)
- Modern chat bubble UI
- Message alignment (left/right)
- Responsive design

---

## 📦 Project Structure

```
customer_support_agent/
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI server
│   ├── agents.py                  # ADK agents & tools
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                 # Container image
│   └── __pycache__/
├── frontend/
│   ├── index.html                 # HTML entry point
│   ├── package.json               # Node dependencies
│   ├── src/
│   │   ├── main.jsx               # React entry
│   │   └── pages/
│   │       ├── Chat.jsx           # Chat component
│   │       └── chat.css           # Styles
│   └── vite.config.js (optional)
├── evaluation/
│   ├── eval_config.json           # Test configuration
│   ├── evalset.json               # Test cases
├── docker-compose.yml             # Multi-container setup
└── README.md                       # This file
```

---

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Docker & Docker Compose** (optional, for containerized setup)
- **Google API Key** (Gemini access)

### Option 1: Local Development (Recommended for Development)

#### Step 1: Environment Setup
```powershell
# Clone or navigate to project
cd c:\Users\drxra\AI_ML\customer_support_agent
```

Create `.env` file:
```
GOOGLE_API_KEY=your_google_api_key_here
SESSION_DB_URL=sqlite:///esa_sessions.db
A2A_API_KEY=my_super_secret_key
AGENT_BASE_URL=http://localhost:8000
```

**⚠️ Security Note**: Never commit `.env` files. Add to `.gitignore`.

#### Step 2: Backend Setup
```powershell
# Create virtual environment
python -m venv .venv

# Activate
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server (auto-reload on file changes)
uvicorn main:app --reload --port 8000
```

Server runs at: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

#### Step 3: Frontend Setup (New Terminal)
```powershell
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

#### Step 4: Test the Integration
1. Open browser: `http://localhost:5173`
2. Type a message: "Tell me about the iPhone 15 Pro"
3. Agent queries product catalog and responds

### Option 2: Docker Setup (Production-like)

```powershell
# Ensure GOOGLE_API_KEY is set in environment
$env:GOOGLE_API_KEY = "your_google_api_key_here"

# Build and run containers
docker-compose up --build

# Access:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:3000 (if configured)
```

### Option 3: Production Deployment

#### Prerequisites
- Kubernetes cluster OR managed container service (GCP Cloud Run, AWS ECS)
- Secret manager (Google Secret Manager, AWS Secrets Manager)
- Persistent database (PostgreSQL recommended over SQLite)

#### Steps
1. **Update `docker-compose.yml`** for your environment
2. **Configure database**:
   ```
   SESSION_DB_URL=postgresql://user:pass@db-host:5432/esa_db
   ```
3. **Set secrets** in your platform's secret manager
4. **Deploy containers** to your infrastructure
5. **Configure HTTPS** with certificate manager
6. **Set up monitoring** (logs, metrics, traces)

---

## 💬 Usage Guide

### Basic Customer Flow

#### Scenario 1: Product Information Query
```
Customer: "What's the price of the Dell XPS 15?"
Agent: "The Dell XPS 15 is priced at $1,299 and we have 45 units in stock."
```

#### Scenario 2: Small Refund (Auto-Approved)
```
Customer: "I want a refund for order ORD-002"
Agent: "I can help with that. The order total was $75. Processing refund..."
Agent: "Refund approved! Refund ID: REF-ORD-002-AUTO"
```

#### Scenario 3: Large Refund (Requires Approval)
```
Customer: "Process a refund of $500 for order ORD-001"
Agent: "I need manager approval for this amount. Submitting request..."
[System waits for human approval]
Manager: [Reviews and approves in backend]
Agent: "Refund approved! Refund ID: REF-ORD-001-HUMAN"
```

### API Reference

#### Send Message
```http
POST /message
Content-Type: application/json

{
  "session_id": "sess_abc123",
  "text": "Tell me about the iPhone 15 Pro",
  "user_id": "user_123"
}
```

**Response:**
```json
{
  "events": 3,
  "responses": [
    "The iPhone 15 Pro is a premium smartphone priced at $999..."
  ],
  "approvals": []
}
```

#### Submit Approval
```http
POST /approve?
  invocation_id=inv_456&
  approval_id=appr_789&
  confirmed=true&
  user_id=user_123&
  session_id=sess_abc123
```

**Response:**
```json
{
  "events": 2,
  "responses": [
    "Refund has been approved and processed."
  ]
}
```

---

## 📊 Evaluation

### Running Tests

Evaluation test cases are defined in `evaluation/evalset.json`:

```bash
# Using ADK CLI
cd evaluation
adk eval --config eval_config.json --set evalset.json

# Or programmatically
python -m adk.eval run --set evalset.json
```

### Test Coverage

| Test Case | Input | Expected Output | Tool Used |
|-----------|-------|-----------------|-----------|
| `product_query_basic` | "Tell me about the iPhone 15 Pro" | Product info returned | product_catalog_lookup |
| `refund_small_auto` | "Refund for order ORD-002 of $50" | Auto-approved | request_refund |

### Adding New Tests

Edit `evaluation/evalset.json`:
```json
{
  "eval_id": "custom_test",
  "conversation": [
    {
      "user_content": {
        "parts": [{"text": "Your test message"}]
      },
      "final_response": {
        "parts": [{"text": "Expected response"}]
      },
      "intermediate_data": {
        "tool_uses": [{"name": "tool_name", "args": {...}}]
      }
    }
  ]
}
```

---

## 🐳 Deployment

### Docker Build

```powershell
# Build image
docker build -t esa-backend:latest ./backend

# Test locally
docker run -e GOOGLE_API_KEY=your_key -p 8000:8000 esa-backend:latest
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | - | Gemini API key |
| `SESSION_DB_URL` | ❌ No | `sqlite:///esa_sessions.db` | Database connection string |
| `A2A_API_KEY` | ❌ No | - | Agent-to-Agent communication key |
| `AGENT_BASE_URL` | ❌ No | `http://localhost:8000` | Base URL for agent callbacks |

### Monitoring & Observability

**Enable Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Track Events:**
- Each runner invocation emits events
- Access via `runner.run_async()` event stream
- Log events to centralized system (Cloud Logging, ELK, etc.)

---

## 📝 Notes & Future Improvements

### Current Limitations
- **Mock Data**: Product and order databases are hardcoded. Replace with real APIs.
- **SQLite**: Not suitable for production. Switch to PostgreSQL.
- **Single Agent Type**: Extend with specialized agents (billing, technical support, etc.)
- **No Authentication**: Implement OAuth2/JWT for security.
- **Limited Error Handling**: Add comprehensive error recovery.

### Future Enhancements

**Phase 2:**
- [ ] Real database integration (PostgreSQL)
- [ ] User authentication & authorization
- [ ] Multi-language support
- [ ] Sentiment analysis for escalation
- [ ] Analytics dashboard

**Phase 3:**
- [ ] Integration with CRM systems (Salesforce, HubSpot)
- [ ] Knowledge base integration
- [ ] Human agent handoff UI
- [ ] SLA tracking & metrics
- [ ] Custom LLM fine-tuning

**Phase 4:**
- [ ] Mobile app (React Native)
- [ ] Voice support (speech-to-text)
- [ ] Multi-modal interactions
- [ ] AI-powered knowledge base generation
- [ ] Predictive customer needs

### Troubleshooting

**Backend won't start:**
```
Error: GOOGLE_API_KEY is missing
→ Check .env file exists and has valid key
```

**Frontend can't connect to backend:**
```
CORS error in browser console
→ Verify backend running on :8000
→ Check CORS middleware is enabled in main.py
```

**Database errors:**
```
SQLAlchemy connection error
→ Ensure DB path is writable
→ Check SESSION_DB_URL format
```

---

## 📚 References

- [Google ADK Documentation](https://cloud.google.com/docs/agents)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Gemini API Guide](https://ai.google.dev/)

---

## 📄 License

This project is part of the Enterprise Agents capstone track.

---

**Last Updated:** November 2025  
**Maintainer:** Ravi Katiyar
