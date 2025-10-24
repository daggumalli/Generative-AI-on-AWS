# Implementation Guide

This guide provides step-by-step instructions to build and deploy the HG2 Hotel Reservation Agentic GenAI application.

## Prerequisites Setup

### 1. AWS Account Configuration

Before starting, ensure you have:
- Active AWS account with appropriate permissions
- AWS CLI installed and configured
- Access to Amazon Bedrock in your region

```bash
# Install AWS CLI (if not already installed)
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Configure AWS credentials
aws configure
```

### 2. Amazon Bedrock Model Access

Enable access to Claude 3.7 Sonnet model:
1. Navigate to Amazon Bedrock console
2. Go to "Model access" in the left sidebar
3. Request access to "Anthropic Claude 3.7 Sonnet"
4. Wait for approval (usually immediate for most regions)

### 3. PostgreSQL Installation

#### Option A: Local PostgreSQL
```bash
# macOS using Homebrew
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb hotels
```

#### Option B: AWS RDS PostgreSQL
```bash
# Create RDS instance using AWS CLI
aws rds create-db-instance \
    --db-instance-identifier hotel-reservations-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username admin \
    --master-user-password YourSecurePassword123 \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-xxxxxxxxx
```

### 4. Python Environment Setup

```bash
# Create virtual environment
python3 -m venv hotel-reservation-env
source hotel-reservation-env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step-by-Step Implementation

### Step 1: Project Structure Setup

```bash
# Clone or create project directory
mkdir hotel-reservations
cd hotel-reservations

# Create directory structure
mkdir -p {database,tools,pages}
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

The requirements.txt includes:
- strands-agents - Core agentic framework
- strands-agents-tools - Additional agent tools
- boto3>=1.40.8 - AWS SDK for Python
- botocore>=1.40.8 - Low-level AWS service access
- bedrock-agentcore<=0.1.5 - Amazon Bedrock AgentCore
- bedrock-agentcore-starter-toolkit==0.1.14 - AgentCore utilities
- aws-opentelemetry-distro~=0.10.1 - AWS observability
- ddgs - DuckDuckGo search integration
- pyyaml - YAML configuration support
- psycopg2-binary - PostgreSQL database adapter
- sqlalchemy - Database ORM
- python-dotenv - Environment variable management
- streamlit - Web application framework

### Step 3: Environment Configuration

Create `.env` file with your configuration:

```bash
# Copy example environment file
cp .env.example .env
```

Update `.env` with your values:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hotels
DB_USER=your_username
DB_PASSWORD=your_password

# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default
```

### Step 4: Database Initialization

```bash
# Initialize database schema
python database/setup.py

# Seed with sample data
python database/seed_data.py
```

This creates:
- 10 hotels across different locations
- 50 rooms with various types and amenities
- Sample reservation data for testing

### Step 5: Agent Configuration

The hotel agent is initialized in `hotel_agent.py` with:

**Model Configuration:**
```python
# Bedrock Claude 3.7 Sonnet model
self.model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.3,
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)
```

**Agent Setup:**
```python
# Agent with tools and system prompt
self.agent = Agent(
    model=self.model,
    tools=[search_hotels, get_available_rooms, make_reservation, 
           get_reservation_details, cancel_reservation, web_search],
    system_prompt=SYSTEM_PROMPT
)
```

**Key Features:**
- Professional hotel reservation assistant persona
- Comprehensive system prompt with clear instructions
- All 6 hotel management tools registered
- Error handling and user-friendly responses
- Interactive chat mode available

### Step 6: Tool Registration

Tools are automatically registered when the agent starts:
- `search_hotels` - Hotel discovery
- `get_available_rooms` - Room availability
- `make_reservation` - Booking creation
- `get_reservation_details` - Reservation lookup
- `cancel_reservation` - Booking cancellation
- `web_search` - External information

### Step 7: Launch Application

```bash
# Start Streamlit application
streamlit run streamlit_app.py --server.port 8501
```

Or use the convenience script:
```bash
python run_streamlit.py
```

## Validation & Testing

### Step 8: Basic Functionality Test

1. **Hotel Search Test**
   ```
   User: "Find hotels in New York with rating above 4.0"
   Expected: List of NYC hotels with ratings ≥ 4.0
   ```

2. **Room Availability Test**
   ```
   User: "Check availability at Grand Plaza Hotel for March 15-18"
   Expected: Available rooms with pricing
   ```

3. **Reservation Test**
   ```
   User: "Book room 102 for March 15-18"
   Expected: Request for guest details, then confirmation
   ```

4. **Reservation Lookup Test**
   ```
   User: "Look up my reservation for john@email.com"
   Expected: Display reservation details
   ```

### Step 9: Database Verification

```sql
-- Check hotels data
SELECT COUNT(*) FROM hotels;

-- Check rooms data
SELECT COUNT(*) FROM rooms;

-- Check reservations
SELECT * FROM reservations LIMIT 5;
```

### Step 10: Agent Response Validation

Monitor agent logs for:
- Tool selection accuracy
- Response coherence
- Error handling
- Performance metrics

## Deployment Considerations

### Production Environment

1. **Database Security**
   - Use AWS RDS with encryption
   - Configure VPC security groups
   - Enable backup and monitoring

2. **Application Hosting**
   - Deploy on AWS ECS or EC2
   - Use Application Load Balancer
   - Configure auto-scaling

3. **Monitoring & Logging**
   - CloudWatch for application logs
   - X-Ray for distributed tracing
   - Custom metrics for agent performance

### Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use AWS Secrets Manager for production
   - Rotate credentials regularly

2. **Database Access**
   - Use IAM database authentication
   - Implement connection pooling
   - Enable query logging

3. **API Security**
   - Implement rate limiting
   - Add input validation
   - Use HTTPS only

## Troubleshooting Common Issues

### Database Connection Issues
```bash
# Test database connection
python -c "from database.setup import test_connection; test_connection()"
```

### Agent Initialization Errors
- Verify Bedrock model access
- Check AWS credentials
- Validate environment variables

### Performance Optimization
- Enable database connection pooling
- Implement caching for frequent queries
- Monitor agent response times

## Next Steps

After successful implementation:
1. Review the [User Guide](USER_GUIDE.md) for usage examples
2. Explore [API Documentation](API_REFERENCE.md) for tool specifications
3. Check [Configuration Guide](CONFIGURATION.md) for customization options

The application should now be running at `http://localhost:8501` with full hotel reservation capabilities.