# document-rag
RAG app for querying documents with LLMs

You will need a working OpenAI API Key to run this app (or equivalent for another LLM in which case you will have to rework the code in rag.py somewhat to match)

## STEPS TO RUN
The frontend and backend are already configured to be connected, you just need to start both of them.
### Frontend
1. From the frontend folder, run 'npm start'.
### Backend
1. Run 'pip install -r requirements.txt' from the backend folder
2. From the src folder, run 'python ./backend/app.py'. It must be run from this folder or the embeddings will not be accessed correctly. 
