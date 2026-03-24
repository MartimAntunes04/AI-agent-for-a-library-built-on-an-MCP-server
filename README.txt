Google API studio: https://aistudio.google.com/app/api-keys~

python -m venv venv
venv\Scripts\activate

# Terminal 1
python mcp_server.py

# Terminal 2
export GEMINI_API_KEY=your-key
python langchain_agent.py


# Terminal 3 - API REST
uvicorn main:app --reload
http://127.0.0.1:8000/docs


# Then open webapp.html in your browser


pip install -U langgraph langchain langchain-google-genai

curl -X POST http://localhost:8000/reset

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'