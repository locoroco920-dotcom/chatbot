# FAQ Chatbot API

A simple FAQ chatbot that uses semantic similarity to answer questions.

## Deployment to Render.com (FREE)

1. Push this code to a GitHub repository
2. Go to https://render.com and sign up (free)
3. Click "New" > "Web Service"
4. Connect your GitHub repo
5. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click "Create Web Service"

Your API will be available at: `https://your-app-name.onrender.com/ask`

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

## API Usage

**Endpoint:** `POST /ask`

**Request Body:**
```json
{
  "question": "When are you open?"
}
```

**Response:**
```json
{
  "answer": "We are open Monday to Friday, 9 AM to 5 PM EST.",
  "confidence": 0.85
}
```
