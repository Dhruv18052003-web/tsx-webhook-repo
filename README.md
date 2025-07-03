# GitHub Webhook Receiver

A Flask-based webhook receiver that captures GitHub repository events (Push, Pull Request, Merge) and stores them in MongoDB.

## Overview

This application provides a webhook endpoint that receives GitHub events and stores them in a MongoDB database. It supports three main GitHub actions:
- **Push**: Code pushed to repository
- **Pull Request**: New pull request submitted
- **Merge**: Pull request merged

## Architecture

```
├── app/
│   ├── libs/           # Core libraries
│   ├── modules/        # Feature modules
│   └── static/         # Static files
├── docs/              # Documentation
└── requirements.txt   # Dependencies
```

## Features

- **Webhook Processing**: Handles GitHub webhook events
- **MongoDB Integration**: Stores events in MongoDB database
- **Logging System**: Comprehensive logging with Loguru
- **Environment Configuration**: Environment-based configuration
- **Static Dashboard**: Web interface to view recent actions

## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (Docker recommended)
- ngrok (for webhook testing)

### Installation

1. **Clone and setup virtual environment**:
```bash
git clone <repository-url>
cd tsk-public-assignment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Setup MongoDB**:
```bash
docker pull mongo
docker run -d --name my-mongo -p 27017:27017 \
  -v mongodbdata:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=Dhruv@1805 mongo
```

4. **Configure environment**:
   - Copy `dev.env` and update MongoDB credentials if needed
   - Default configuration connects to local MongoDB

5. **Run application**:
```bash
python app.py
```

### Setup GitHub Webhook

1. **Expose local server**:
```bash
ngrok http 5000
```

2. **Configure GitHub webhook**:
   - Go to your GitHub repository → Settings → Webhooks
   - Add webhook URL: `https://your-ngrok-url.ngrok.io/v1/git/[action]`
   - Set content type: `application/json`
   - Select events: Push, Pull, Merge requests

## API Endpoints

### System Endpoints
- `GET /` - Welcome message
- `GET /v1/sys/echo` - Echo query parameters

### Git Webhook Endpoints
- `POST /v1/git/push` - Receive push events
- `POST /v1/git/pull` - Receive pull request events  
- `POST /v1/git/merge` - Receive merge events
- `GET /v1/git/list` - List recent actions

### Static Files
- `GET /static/index.html` - Dashboard to view recent actions

## Configuration

Environment variables in `dev.env`:

```env
# MongoDB
DB_PROTOCOL=mongodb
DB_HOST=localhost
DB_PORT=27017
DB_USERNAME=admin
DB_PASSWORD=Dhruv@1805
DB_NAME=techstax

# Logging
STORAGE_PATH=../storage
LOG_PATH=logs
APP_LOG_PATH=app
SYS_LOG_PATH=sys
```

## Database Schema

**Collection**: `git_action_logs`

```json
{
  "_id": "ObjectId",
  "request_id": "string",
  "author": "string", 
  "action": "PUSH|PULL|MERGE",
  "from_branch": "string",
  "to_branch": "string",
  "timestamp": "datetime"
}
```

## Logging

The application uses Loguru for structured logging:

- **App Logs**: `../storage/logs/app/`
  - `debug.log` - Debug information
  - `info.log` - General information
  - `error.log` - Error messages

- **System Logs**: `../storage/logs/sys/`
  - `sys.log` - Request/response logs

## Testing

### Manual Testing

1. **Test system endpoints**:
```bash
curl http://localhost:5000/
curl "http://localhost:5000/v1/sys/echo?fname=John&lname=Doe"
```

2. **Test webhook simulation**:
```bash
curl -X POST http://localhost:5000/v1/git/push \
  -H "Content-Type: application/json" \
  -d '{"head_commit":{"id":"abc123"},"pusher":{"name":"testuser"},"ref":"refs/heads/main","repository":{"default_branch":"main"}}'
```

3. **View recent actions**:
```bash
curl http://localhost:5000/v1/git/list
```

### Web Dashboard

Visit `http://localhost:5000/static/index.html` to view recent repository actions in a web interface.

## Deployment

### Production Considerations

1. **Use Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Environment Security**:
   - Use production MongoDB credentials
   - Set secure environment variables
   - Enable HTTPS for webhook endpoints

3. **MongoDB Security**:
   - Use authentication
   - Configure network access
   - Regular backups

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**:
   - Verify MongoDB is running: `docker ps`
   - Check credentials in `dev.env`
   - Ensure port 27017 is accessible

2. **Webhook Not Receiving Events**:
   - Verify ngrok is running and URL is correct
   - Check GitHub webhook configuration
   - Review webhook delivery logs in GitHub

3. **Import Errors**:
   - Ensure virtual environment is activated
   - Install all requirements: `pip install -r requirements.txt`

### Logs Location

Check application logs in:
- `../storage/logs/app/` - Application logs
- `../storage/logs/sys/` - System/request logs

## Contributing

1. Follow existing code structure
2. Add appropriate logging
3. Update documentation for new features
4. Test webhook endpoints thoroughly

## License

This project is part of a technical assessment for TechStaX.