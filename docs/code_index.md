# Code Index

This document provides a comprehensive overview of the codebase structure and key components.

## Project Structure

```
tsk-public-assignment/
├── app/                    # Main application package
│   ├── libs/              # Core libraries and utilities
│   │   ├── config.py      # Configuration management
│   │   ├── logger.py      # Logging configuration
│   │   └── route.py       # Route registration
│   ├── modules/           # Feature modules
│   │   ├── git/          # Git webhook handling
│   │   │   ├── controllers/
│   │   │   │   └── actions.py    # Git webhook controllers
│   │   │   └── models/
│   │   │       └── actions.py    # Git data models
│   │   └── sys/          # System utilities
│   │       └── controllers/
│   │           └── sys.py        # System controllers
│   ├── static/           # Static web files
│   │   └── index.html    # Dashboard interface
│   └── __init__.py       # Package initialization
├── docs/                 # Documentation
│   ├── readme.md         # Project documentation
│   └── code_index.md     # This file
├── app.py               # Application entry point
├── dev.env              # Environment configuration
├── requirements.txt     # Python dependencies
└── README.md           # Setup instructions
```

## Core Components

### 1. Application Entry Point

#### `app.py`
- **Purpose**: Flask application initialization and configuration
- **Key Functions**:
  - Creates Flask app with static folder configuration
  - Registers all routes via `register_all_routes()`
  - Loads configuration from `Config` class
  - Sets up logging with Loguru
  - Implements request logging middleware

```python
# Key features:
- Flask app creation with static folder
- Route registration
- Configuration loading
- Request logging middleware
```

### 2. Core Libraries (`app/libs/`)

#### `config.py`
- **Purpose**: Centralized configuration management
- **Key Features**:
  - Loads environment variables from `dev.env`
  - MongoDB connection string construction
  - File path configuration for logs and storage
  - Environment-specific settings

```python
# Key components:
- Environment file loading with dotenv
- MongoDB connection string building
- Storage and logging path configuration
- URL encoding for database credentials
```

#### `logger.py`
- **Purpose**: Logging system configuration using Loguru
- **Key Features**:
  - Multiple log levels (DEBUG, INFO, ERROR)
  - Separate log files for different purposes
  - System-specific logging with filtering
  - Console output for development

```python
# Logging structure:
- App logs: debug.log, info.log, error.log
- System logs: sys.log (for requests)
- Console output in development mode
- Log rotation (1 MB per file)
```

#### `route.py`
- **Purpose**: Route registration and URL mapping
- **Key Features**:
  - Blueprint-based route organization
  - Modular route registration
  - URL prefix management

```python
# Route groups:
- Root routes: / (home)
- System routes: /v1/sys/* (echo)
- Git routes: /v1/git/* (webhooks, list)
```

### 3. Git Module (`app/modules/git/`)

#### `controllers/actions.py`
- **Purpose**: GitHub webhook event handling
- **Key Functions**:
  - `pull()` - Handles pull request webhooks
  - `push()` - Handles push event webhooks  
  - `merge()` - Handles merge event webhooks
  - `list()` - Returns recent repository actions

```python
# Webhook processing:
- Content-Type validation
- JSON payload parsing
- Error handling with stack traces
- MongoDB document creation
- Standardized response format
```

#### `models/actions.py`
- **Purpose**: Data access layer for git actions
- **Key Functions**:
  - `create(doc)` - Inserts new action document
  - `latest(limit)` - Retrieves recent actions with formatting

```python
# Database operations:
- MongoDB connection management
- Document insertion
- Query with sorting and limiting
- Timestamp formatting for display
```

### 4. System Module (`app/modules/sys/`)

#### `controllers/sys.py`
- **Purpose**: System utility endpoints
- **Key Functions**:
  - `home()` - Welcome message endpoint
  - `echo()` - Query parameter echo service

```python
# Utility functions:
- Simple text responses
- Query parameter processing
- JSON response formatting
```

## Data Flow

### 1. Webhook Processing Flow
```
GitHub Event → Flask Route → Controller → Model → MongoDB
                    ↓
              Logging System → Log Files
```

### 2. Request Processing
```
HTTP Request → app.py middleware → Route Blueprint → Controller → Response
                     ↓
               System Logging → sys.log
```

## Key Design Patterns

### 1. MVC Architecture
- **Models**: Data access layer (`models/actions.py`)
- **Views**: JSON responses from controllers
- **Controllers**: Business logic (`controllers/actions.py`)

### 2. Blueprint Pattern
- Modular route organization
- Namespace separation (`/v1/sys`, `/v1/git`)
- Easy route management and scaling

### 3. Configuration Pattern
- Environment-based configuration
- Centralized settings management
- Secure credential handling

### 4. Logging Pattern
- Structured logging with Loguru
- Multiple log levels and files
- Request/response tracking
- Development vs production logging

## Database Schema

### Collection: `git_action_logs`
```json
{
  "_id": "ObjectId",
  "request_id": "string",     // Unique identifier from GitHub
  "author": "string",         // GitHub username
  "action": "string",         // PUSH|PULL|MERGE
  "from_branch": "string",    // Source branch
  "to_branch": "string",      // Target branch  
  "timestamp": "datetime"     // UTC timestamp
}
```

## API Endpoints

### System Endpoints
| Method | Endpoint | Purpose | Controller |
|--------|----------|---------|------------|
| GET | `/` | Welcome message | `sys.home()` |
| GET | `/v1/sys/echo` | Echo parameters | `sys.echo()` |

### Git Webhook Endpoints
| Method | Endpoint | Purpose | Controller |
|--------|----------|---------|------------|
| POST | `/v1/git/push` | Push events | `actions.push()` |
| POST | `/v1/git/pull` | Pull requests | `actions.pull()` |
| POST | `/v1/git/merge` | Merge events | `actions.merge()` |
| GET | `/v1/git/list` | Recent actions | `actions.list()` |

## Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (invalid payload)
- `415` - Unsupported Media Type
- `500` - Internal Server Error

### Error Response Format
```json
{
  "action": "string",
  "error": "string", 
  "stacktrace": "string"
}
```

## Dependencies

### Core Dependencies
- **Flask 3.1.1** - Web framework
- **PyMongo 4.13.2** - MongoDB driver
- **Loguru 0.7.3** - Logging library
- **python-dotenv 1.1.1** - Environment variables

### Supporting Libraries
- **flask-cors 6.0.1** - CORS handling
- **Flask-PyMongo 3.0.1** - Flask-MongoDB integration
- **dnspython 2.7.0** - DNS resolution for MongoDB

## Environment Configuration

### Required Variables (`dev.env`)
```env
# Database
DB_PROTOCOL=mongodb
DB_HOST=localhost
DB_PORT=27017
DB_USERNAME=admin
DB_PASSWORD=Dhruv@1805
DB_NAME=techstax

# Storage
STORAGE_PATH=../storage
LOG_PATH=logs
APP_LOG_PATH=app
SYS_LOG_PATH=sys
```

## Security Considerations

### 1. Input Validation
- Content-Type header validation
- JSON payload validation
- Required field checking

### 2. Error Handling
- Graceful error responses
- Stack trace logging
- No sensitive data exposure

### 3. Database Security
- Connection string encoding
- Credential management via environment variables
- MongoDB authentication

## Testing Strategy

### 1. Manual Testing
- Direct endpoint testing with curl
- Webhook simulation
- Database verification

### 2. Integration Testing
- GitHub webhook integration
- MongoDB connectivity
- Log file generation

## Deployment Notes

### Development
- Debug mode disabled
- Console logging enabled
- Local MongoDB connection

### Production Considerations
- Use Gunicorn WSGI server
- Secure MongoDB credentials
- HTTPS for webhook endpoints
- Log rotation and monitoring