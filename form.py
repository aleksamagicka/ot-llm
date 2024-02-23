# importing Flask and other modules
import time

from flask import Flask, request, render_template, Response, stream_with_context

# Flask constructor
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        def stream_results():
            yield 'Hello '
            time.sleep(1)
            yield request.form.get("fname")
            time.sleep(1)
            yield '!'

        return Response(stream_with_context(stream_results()))

    return render_template("form.html")


if __name__ == '__main__':
    app.run()