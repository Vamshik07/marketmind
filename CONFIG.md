# MarketAI Suite - Configuration Guide

## Environment Setup

### 1. Get Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up or login to your account
3. Navigate to the **API Keys** section
4. Click **Create API Key**
5. Copy the generated key
6. Store it securely in `.env` file

### 2. Create .env File

Create a file named `.env` in the project root directory with:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Security Note**: Never commit `.env` to version control. It's already included in `.gitignore`.

### 3. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

Required packages:
- **Flask 3.0.0** - Web framework
- **Groq 0.4.1** - Groq AI API client
- **python-dotenv 1.0.0** - Environment variable loader

### 4. Run the Application

```bash
# Start Flask development server
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## Configuration Options

### Flask Configuration

Edit `app.py` to modify:

```python
# Debug mode (default: True)
app.run(debug=True)

# Host (default: 127.0.0.1)
app.run(host='127.0.0.1')

# Port (default: 5000)
app.run(port=5000)
```

### AI Model Configuration

Edit `backend/ai_engine.py` to change:

```python
# Model selection
model="llama-3.1-8b-instant"  # Fast, lightweight
model="llama-3.3-70b-versatile"  # More powerful

# Temperature (0-1, default: 0.7)
temperature=0.7  # Lower = more deterministic, Higher = more creative

# Max tokens (default: 2000)
max_tokens=2000  # Response length limit
```

### Prompt Customization

Edit `backend/prompts.py` to customize:

- Campaign generation prompts
- Sales pitch creation prompts
- Lead scoring prompts

## Groq API Models Available

### Fast & Lightweight
- `llama-3.1-8b-instant` - Best for quick responses
- `mixtral-8x7b-32768` - Good balance

### Powerful & Detailed
- `llama-3.3-70b-versatile` - Best for complex tasks
- `llama-3.1-70b-versatile` - High quality responses

## API Rate Limiting

Groq API has rate limits based on your plan:
- Check your usage at: https://console.groq.com/usage
- Monitor tokens per minute (TPM)
- Monitor requests per minute (RPM)

## Troubleshooting Configuration

### Issue: ModuleNotFoundError

```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: GROQ_API_KEY not found

```bash
# Verify .env file location
ls -la .env

# Verify content
cat .env

# Check if key is valid
echo $GROQ_API_KEY
```

### Issue: Port 5000 already in use

```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
# Edit app.py: app.run(port=5001)
```

### Issue: Flask app not starting

```bash
# Check Python version
python --version  # Should be 3.8+

# Verify Flask installation
pip show flask

# Run with verbose output
python -u app.py
```

## Security Best Practices

1. **API Key Protection**
   - Never share your API key
   - Never commit `.env` to git
   - Rotate API keys periodically

2. **Environment Variables**
   - Use different keys for development and production
   - Store production keys in secure vaults
   - Use environment-specific .env files

3. **HTTPS in Production**
   - Enable SSL/TLS certificates
   - Use proxy servers (Nginx, Apache)
   - Set secure cookies

4. **Input Validation**
   - Validate all user inputs
   - Sanitize text before sending to AI
   - Limit request sizes

## Performance Optimization

### Caching
```python
# Add caching for similar requests
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_response(prompt):
    return generate_response(prompt)
```

### Connection Pooling
```python
# Reuse HTTP connections
import requests
session = requests.Session()
```

### Async Processing
```python
# Use async for faster responses
import asyncio
from flask import Flask
```

## Monitoring & Logging

Add logging to track API calls:

```python
import logging

logging.basicConfig(
    filename='marketai.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Database Setup (Optional)

To store historical requests:

```bash
# Install database
pip install flask-sqlalchemy

# Create database file
touch instance/marketai.db
```

## Deployment Checklist

- [ ] Set `debug=False` in production
- [ ] Use strong secret key for sessions
- [ ] Configure CORS if needed
- [ ] Set up HTTPS
- [ ] Enable rate limiting
- [ ] Monitor API usage
- [ ] Set up error logging
- [ ] Configure backup procedures
- [ ] Test all features
- [ ] Document API endpoints

## Support & Help

- Check logs: `tail -f marketai.log`
- Test API key: https://console.groq.com/keys
- Review Groq docs: https://console.groq.com/docs
- Check Flask docs: https://flask.palletsprojects.com/

---

**Last Updated**: January 30, 2026
**Version**: 1.0.0