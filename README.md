# 🤖 Generative AI on AWS

A collection of advanced Generative AI applications and demonstrations built on AWS services, showcasing cutting-edge AI agent patterns and real-world implementations.

**Demo**
https://www.youtube.com/watch?v=IJmfIONe3Ws

## 🎯 **Projects**

### 🏨 **Hotel Reservations - AI Agentic Application**
**Location**: [`hotel-reservations/`](./hotel-reservations/)

A complete AI-powered hotel reservation system demonstrating advanced agentic AI patterns:

- **🤖 AI Agent**: Claude 3.7 Sonnet with AWS Bedrock + AgentCore + Strands
- **🛠️ 6 Specialized Tools**: Search, availability, booking, management, cancellation, web search
- **💻 Web Interface**: Streamlit chat app with admin panel
- **🗄️ Database**: PostgreSQL with sample hotels and reservations
- **📊 Real-world Demo**: Complete booking lifecycle management

**Key Features:**
- Natural language hotel search and booking
- Intelligent tool orchestration and decision making
- Real-time availability checking and reservation management
- Admin panel for hotel and booking management
- Comprehensive documentation and testing

**Quick Start:**
```bash
cd hotel-reservations/
pip install -r requirements.txt
python database/setup.py
python run_streamlit.py
```

**Live Demo**: http://localhost:8501

---

## 🚀 **Technologies Used**

### **AWS Services**
- **AWS Bedrock**: Foundation models (Claude 3.7 Sonnet)
- **AgentCore**: Enterprise AI agent framework
- **AWS CLI**: Authentication and configuration

### **AI Frameworks**
- **Strands**: Tool orchestration and conversation management
- **Anthropic Claude**: Advanced reasoning and natural language processing

### **Development Stack**
- **Python 3.8+**: Core development language
- **Streamlit**: Modern web interface framework
- **PostgreSQL**: Production-ready database
- **Rich**: Beautiful CLI interfaces and logging

## 🏗️ **Architecture Patterns**

### **Agentic AI Design**
- **Tool-based Architecture**: Modular, reusable AI tools
- **Context Management**: Conversation state and memory
- **Error Handling**: Graceful degradation and recovery
- **Natural Language Interface**: Chat-based user interaction

### **Enterprise Patterns**
- **Database Integration**: Real-time data operations
- **Web Interface**: Production-ready user experience
- **Admin Capabilities**: Management and monitoring tools
- **Testing Framework**: Comprehensive validation and testing

## 📚 **Learning Resources**

Each project includes comprehensive documentation:
- **Architecture Guides**: System design and component interaction
- **Implementation Guides**: Step-by-step setup and deployment
- **API Documentation**: Tool interfaces and data models
- **Testing Examples**: Validation and quality assurance

## 🎯 **Use Cases Demonstrated**

### **Business Applications**
- **Customer Service Automation**: AI-powered booking assistance
- **Process Automation**: Intelligent workflow orchestration
- **Data Integration**: Real-time database operations
- **User Experience**: Natural language interfaces

### **Technical Demonstrations**
- **Agentic AI Patterns**: Tool selection and orchestration
- **AWS Integration**: Enterprise cloud services
- **Modern Web Development**: Responsive user interfaces
- **Database Design**: Scalable data architecture

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+
- AWS Account with Bedrock access
- PostgreSQL (for hotel-reservations)
- AWS CLI configured

### **Quick Setup**
```bash
# Clone the repository
git clone https://github.com/daggumalli/Generative-AI-on-AWS.git
cd Generative-AI-on-AWS

# Choose a project
cd hotel-reservations/

# Follow project-specific setup instructions
```

## 🤝 **Contributing**

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see individual project LICENSE files for details.

## 🆘 **Support**

- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: Comprehensive guides and examples

---

**🎉 Explore the future of AI-powered applications with real-world implementations on AWS!**
