from flask import Flask, render_template, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)

# Fix for Jinja cache bug
@app.before_request
def fix_request_args():
    if not isinstance(request.args, ImmutableMultiDict):
        request.args = ImmutableMultiDict(request.args)

@app.route('/')
def home():
    name = request.args.get('name', 'Guest')
    return render_template('index.html', name=name)

@app.route('/api/test')
def api_test():
    return jsonify({
        "status": "success",
        "message": "Flask app with Jinja fix is working!",
        "args": dict(request.args)
    })

if __name__ == '__main__':
    app.run(debug=True)
