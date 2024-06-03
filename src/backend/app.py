from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import services.rag as rag

app = Flask(__name__, static_folder='frontend/public')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/run_rag', methods=['POST'])
def run_rag():
    data = request.json
    result = rag.get_instructions(data['data'])
    print(result)
    return jsonify(result)
    
if __name__ == '__main__':
    app.run(debug=True)