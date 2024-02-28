# importing Flask and other modules
import datetime
import os
import time

from dkg import DKG
from dkg.providers import NodeHTTPProvider, BlockchainProvider
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, render_template, Response, stream_with_context
from langchain_openai import ChatOpenAI

from langchain.schema import (
    HumanMessage,
    SystemMessage
)

from consts import SPARQL_GENERATION_SELECT_TEMPLATE
import env

# Flask constructor
app = Flask(__name__)

load_dotenv(find_dotenv())

print("Initializing...")

def log_to_file(message):
    log_file = open("logger.log", "a")
    log_file.write(f"[{datetime.datetime.utcnow().isoformat()}] {message}\n")
    log_file.close()


chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=env.OPENAI_API_KEY)

jwt_token = env.JWT_TOKEN
node_provider = NodeHTTPProvider(env.NODE_URL, jwt_token)
blockchain_provider = BlockchainProvider(
    "mainnet",
    "otp:2043",
)

dkg = DKG(node_provider, blockchain_provider)
try:
    print(dkg.node.info)
    log_to_file(dkg.node.info)
except:
    msg = "Error: couldn't connect to DKG node!"
    print(msg)
    log_to_file(msg)
    exit()


@app.route('/', methods=["GET", "POST"])
def main_route():
    if request.method == "POST":
        query_text = request.form.get("query")

        def stream_results():
            yield f"Input: {query_text}</br></br>"
            log_to_file(f"Received input: [{query_text}]")

            yield 'Requesting SPARQL from GPT, please wait (can take a long time)...</br></br>'

            messages = [
                SystemMessage(content=SPARQL_GENERATION_SELECT_TEMPLATE),
                HumanMessage(content=query_text)
            ]

            response = chat(messages)
            cleaned_sparql = response.content.replace("```", "")

            log_to_file(f"Received SPARQL code: [{cleaned_sparql}]")

            yield f"<code>{cleaned_sparql}</code>"
            yield '</br></br>SPARQL received. Querying DKG, please wait...</br></br>'

            yield "<a href='javascript:history.back();'>[Go Back]</a></br></br>"

            try:
                result = dkg.graph.query(cleaned_sparql, repository="privateCurrent")
                yield f"<code>{result}</code>"

                log_to_file(f"Received DKG result: {result}")
            except Exception as error:
                yield f"SPARQL query failed! {repr(error)}"
                log_to_file(f"SPARQL query failed! Stack trace: {repr(error)}")

            yield "</br></br><a href='javascript:history.back();'>[Go Back]</a>"

        return Response(stream_with_context(stream_results()))

    return render_template("form.html")


if __name__ == '__main__':
    app.run()
