from flask import Flask

# Create a new Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Simple Flask App Test</h1>
    <p>This is a minimal Flask application to test routing.</p>
    <ul>
        <li><a href="/hello">Hello Route</a></li>
        <li><a href="/genai">GenAI Route</a></li>
        <li><a href="/test">Test Route</a></li>
    </ul>
    """

@app.route('/hello')
def hello():
    return "Hello, World! This route is working."

@app.route('/genai')
def genai():
    return "GenAI route is working in the simple app."

@app.route('/test')
def test():
    return "Test route is working in the simple app."

if __name__ == '__main__':
    print("Starting Simple Flask Test App...")
    print("Access at http://localhost:5000 or http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 