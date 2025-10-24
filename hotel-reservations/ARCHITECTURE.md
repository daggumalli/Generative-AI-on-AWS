# HG2 Hotel Reservations - Conceptual Architecture

## 🏗️ **High-Level Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERACTION LAYER                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │   Web Browser   │    │   Mobile App    │    │   API Client    │            │
│  │   (Chrome/FF)   │    │   (Future)      │    │   (Future)      │            │
│  └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘            │
│            │                      │                      │                    │
│            └──────────────────────┼──────────────────────┘                    │
│                                   │                                           │
└───────────────────────────────────┼───────────────────────────────────────────┘
                                    │ HTTP/WebSocket
                                    │
┌───────────────────────────────────▼───────────────────────────────────────────┐
│                           PRESENTATION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        Streamlit Web Framework                          │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │   Chat UI       │  │   Admin Panel   │  │   Sidebar       │        │   │
│  │  │   - Messages    │  │   - Statistics  │  │   - Examples    │        │   │
│  │  │   - Input       │  │   - Management  │  │   - Status      │        │   │
│  │  │   - History     │  │   - Analytics   │  │   - Help        │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└───────────────────────────────────┼───────────────────────────────────────────┘
                                    │ Python Function Calls
                                    │
┌───────────────────────────────────▼───────────────────────────────────────────┐
│                            APPLICATION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      HG2 Hotel Agent Core                              │   │
│  │                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Strands Agent Framework                      │   │   │
│  │  │                                                                 │   │   │
│  │  │  ┌─────────────────┐    ┌─────────────────────────────────┐    │   │   │
│  │  │  │  Agent Engine   │    │        System Prompt           │    │   │   │
│  │  │  │  - Reasoning    │    │  - Role Definition             │    │   │   │
│  │  │  │  - Planning     │    │  - Behavior Guidelines        │    │   │   │
│  │  │  │  - Execution    │    │  - Tool Usage Instructions    │    │   │   │
│  │  │  └─────────────────┘    └─────────────────────────────────┘    │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└───────────────────────────────────┼───────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼───────────────────────────────────────────┐
│                              TOOLS LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │  Hotel Tools    │  │  Search Tools   │  │  Utility Tools  │                │
│  │                 │  │                 │  │                 │                │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │                │
│  │ │search_hotels│ │  │ │ web_search  │ │  │ │ validation  │ │                │
│  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │                │
│  │ ┌─────────────┐ │  │                 │  │ ┌─────────────┐ │                │
│  │ │get_rooms    │ │  │                 │  │ │ formatting  │ │                │
│  │ └─────────────┘ │  │                 │  │ └─────────────┘ │                │
│  │ ┌─────────────┐ │  │                 │  │ ┌─────────────┐ │                │
│  │ │make_booking │ │  │                 │  │ │ error_handle│ │                │
│  │ └─────────────┘ │  │                 │  │ └─────────────┘ │                │
│  │ ┌─────────────┐ │  │                 │  │                 │                │
│  │ │get_details  │ │  │                 │  │                 │                │
│  │ └─────────────┘ │  │                 │  │                 │                │
│  │ ┌─────────────┐ │  │                 │  │                 │                │
│  │ │cancel_res   │ │  │                 │  │                 │                │
│  │ └─────────────┘ │  │                 │  │                 │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│                                                                                 │
└─────────────────────────┼─────────────────────┼─────────────────────────────────┘
                          │                     │
                          │                     │
┌─────────────────────────▼───────────────────┐ │
│            DATA LAYER                       │ │
├─────────────────────────────────────────────┤ │
│                                             │ │
│  ┌─────────────────────────────────────┐   │ │
│  │         PostgreSQL Database         │   │ │
│  │                                     │   │ │
│  │  ┌─────────────┐ ┌─────────────┐   │   │ │
│  │  │   Hotels    │ │    Rooms    │   │   │ │
│  │  │   Table     │ │    Table    │   │   │ │
│  │  │             │ │             │   │   │ │
│  │  │ - id        │ │ - id        │   │   │ │
│  │  │ - name      │ │ - hotel_id  │   │   │ │
│  │  │ - address   │ │ - room_num  │   │   │ │
│  │  │ - city      │ │ - type      │   │   │ │
│  │  │ - state     │ │ - price     │   │   │ │
│  │  │ - rating    │ │ - occupancy │   │   │ │
│  │  │ - amenities │ │ - amenities │   │   │ │
│  │  └─────────────┘ └─────────────┘   │   │ │
│  │                                     │   │ │
│  │  ┌─────────────────────────────┐   │   │ │
│  │  │      Reservations Table     │   │   │ │
│  │  │                             │   │   │ │
│  │  │ - id                        │   │   │ │
│  │  │ - room_id                   │   │   │ │
│  │  │ - guest_name                │   │   │ │
│  │  │ - guest_email               │   │   │ │
│  │  │ - check_in_date             │   │   │ │
│  │  │ - check_out_date            │   │   │ │
│  │  │ - total_amount              │   │   │ │
│  │  │ - status                    │   │   │ │
│  │  └─────────────────────────────┘   │   │ │
│  └─────────────────────────────────────┘   │ │
│                                             │ │
└─────────────────────────────────────────────┘ │
                                                │
┌───────────────────────────────────────────────▼─┐
│              EXTERNAL SERVICES                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │            Amazon Bedrock               │   │
│  │                                         │   │
│  │  ┌─────────────────────────────────┐   │   │
│  │  │      Claude 3.7 Sonnet         │   │   │
│  │  │                                 │   │   │
│  │  │ - Natural Language Processing   │   │   │
│  │  │ - Reasoning & Planning          │   │   │
│  │  │ - Tool Selection & Usage        │   │   │
│  │  │ - Response Generation           │   │   │
│  │  └─────────────────────────────────┘   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │         DuckDuckGo Search API           │   │
│  │                                         │   │
│  │ - Web Search Results                    │   │
│  │ - Travel Information                    │   │
│  │ - Local Attractions                     │   │
│  │ - Weather Data                          │   │
│  │ - Restaurant Recommendations           │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 🔄 **Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              REQUEST FLOW                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

User Input → Streamlit UI → Agent Core → Tool Selection → Data Processing → Response

1. 👤 User types: "Find hotels in New York"
   ↓
2. 🌐 Streamlit captures input and calls agent
   ↓
3. 🤖 Strands Agent processes natural language
   ↓
4. 🧠 Claude 3.7 analyzes intent and selects tools
   ↓
5. 🔧 search_hotels() tool executes
   ↓
6. 🗄️ PostgreSQL query: SELECT * FROM hotels WHERE city = 'New York'
   ↓
7. 📊 Results formatted and returned
   ↓
8. 🤖 Agent generates natural language response
   ↓
9. 🌐 Streamlit displays response to user

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            COMPONENT INTERACTIONS                              │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    HTTP     ┌─────────────┐    Function    ┌─────────────┐
│   Browser   │◄──────────►│  Streamlit  │◄─────────────►│    Agent    │
└─────────────┘             └─────────────┘                └─────────────┘
                                                                   │
                                                            Function Calls
                                                                   │
                                                                   ▼
┌─────────────┐    HTTPS    ┌─────────────┐    SQL        ┌─────────────┐
│   Bedrock   │◄──────────►│    Tools    │◄─────────────►│ PostgreSQL  │
│   Claude    │             │   Layer     │                │  Database   │
└─────────────┘             └─────────────┘                └─────────────┘
                                   │
                            HTTP API Calls
                                   │
                                   ▼
                            ┌─────────────┐
                            │ DuckDuckGo  │
                            │   Search    │
                            └─────────────┘
```

## 🏛️ **Layered Architecture Pattern**

### **Layer 1: Presentation Layer**
- **Technology**: Streamlit
- **Responsibility**: User interface, session management, input/output handling
- **Components**: Chat interface, admin panel, sidebar navigation

### **Layer 2: Application Layer**
- **Technology**: Strands Agents Framework
- **Responsibility**: Business logic, agent orchestration, conversation management
- **Components**: Agent engine, system prompts, conversation state

### **Layer 3: Service Layer**
- **Technology**: Custom Python tools
- **Responsibility**: Business operations, data processing, external integrations
- **Components**: Hotel tools, search tools, validation utilities

### **Layer 4: Data Access Layer**
- **Technology**: SQLAlchemy + psycopg2
- **Responsibility**: Database operations, query optimization, connection management
- **Components**: Database models, connection utilities, query builders

### **Layer 5: Data Layer**
- **Technology**: PostgreSQL
- **Responsibility**: Data persistence, integrity, relationships
- **Components**: Hotels, rooms, reservations tables

### **Layer 6: External Services Layer**
- **Technology**: REST APIs, Cloud services
- **Responsibility**: AI processing, web search, external data
- **Components**: Amazon Bedrock, DuckDuckGo API

## 🔧 **Technology Stack Mapping**

```
┌─────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend:     Streamlit + HTML/CSS + JavaScript               │
│  Backend:      Python 3.12 + Strands Agents                   │
│  AI/ML:        Amazon Bedrock + Claude 3.7 Sonnet             │
│  Database:     PostgreSQL 15 + SQLAlchemy                      │
│  Search:       DuckDuckGo Search API                           │
│  Config:       python-dotenv + Environment Variables           │
│  Deployment:   Local Development (Homebrew + pip)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔐 **Security Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Authentication:  AWS Credentials (IAM)                        │
│  Authorization:   AWS IAM Policies                             │
│  Data Security:   PostgreSQL Local Access                      │
│  Transport:       HTTPS (AWS APIs), Local HTTP (Development)   │
│  Input Validation: SQL Injection Prevention                    │
│  Error Handling:  Graceful Degradation                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 **Scalability Considerations**

### **Current Architecture (Development)**
- **Users**: Single user (localhost)
- **Concurrency**: Single session
- **Database**: Local PostgreSQL
- **AI**: Shared AWS Bedrock (rate limited)

### **Production Architecture (Future)**
- **Users**: Multi-tenant
- **Concurrency**: Load balancing
- **Database**: Cloud PostgreSQL (RDS)
- **AI**: Dedicated Bedrock capacity
- **Caching**: Redis for session management
- **Monitoring**: CloudWatch + OpenTelemetry

## 🎯 **Key Architectural Decisions**

1. **Monolithic Design**: Single application for simplicity
2. **Local Development**: All components on localhost
3. **Agent-First**: AI agent as the primary interface
4. **Tool-Based**: Modular tool architecture
5. **Database-Driven**: PostgreSQL for data persistence
6. **Cloud AI**: Leverage AWS Bedrock for intelligence
7. **Web-First**: Streamlit for rapid UI development

This architecture provides a solid foundation for a hotel reservations system with AI capabilities while maintaining simplicity for development and testing.