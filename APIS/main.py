import os
import pickle
import openai
from flask import Flask, request, jsonify

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import VectorStoreIndex, download_loader

# Initialize Flask application
app = Flask(__name__)

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = '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'
openai.api_key = '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'

# Authorize Google Docs
def authorize_gdocs():
    google_oauth2_scopes = [
        "https://www.googleapis.com/auth/documents.readonly"
    ]
    cred = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", google_oauth2_scopes)
            cred = flow.run_local_server(port=0)
        with open("token.pickle", 'wb') as token:
            pickle.dump(cred, token)

# API endpoint for query
@app.route('/query', methods=['GET'])
def query():
    prompt = request.args.get('prompt', '')
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return jsonify(response)

if __name__ == '__main__':
    # Authorize Google Docs
    authorize_gdocs()

    # Load GoogleDocsReader and documents
    GoogleDocsReader = download_loader('GoogleDocsReader')
    gdoc_ids = ['1esD5gleapNkH-EHHPmEa0GExfZ68M_79AFBVuf7gbaA']
    loader = GoogleDocsReader()
    documents = loader.load_data(document_ids=gdoc_ids)
    index = VectorStoreIndex.from_documents(documents)

    # Run Flask application
    app.run()
