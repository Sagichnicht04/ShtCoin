from flask import Flask, render_template_string, Response
import time

app = Flask(__name__)

FILE_PATH = "log.txt"

HTML_TEMPLATE = ""


@app.route('/')
def index():
    with open("index.html", "r") as file:
        HTML_TEMPLATE = file.read()
    return render_template_string(HTML_TEMPLATE)

@app.route('/stream')
def stream():
    def generate():
        last_content = ""
        while True:
            try:
                with open(FILE_PATH, 'r') as f:
                    content = f.read().split('\n')[-1].strip()
                    if content != last_content:
                        last_content = content
                        yield f"data: {content}\n\n"
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
