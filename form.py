# importing Flask and other modules
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

# Flask constructor
app = Flask(__name__)

load_dotenv(find_dotenv())

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

jwt_token = os.environ['jwt_token']
node_provider = NodeHTTPProvider(os.environ['node_url'], jwt_token)
blockchain_provider = BlockchainProvider(
    "mainnet",
    "otp:2043",
)

dkg = DKG(node_provider, blockchain_provider)
try:
    print(dkg.node.info)
except:
    print("Error: couldn't connect to DKG node!")
    exit()


@app.route('/', methods=["GET", "POST"])
def main_route():
    if request.method == "POST":
        query_text = request.form.get("query")

        def stream_results():
            yield 'Requesting SPARQL from GPT, please wait...</br></br>'

            messages = [
                SystemMessage(content=SPARQL_GENERATION_SELECT_TEMPLATE),
                HumanMessage(content=query_text)
            ]

            response = chat(messages)
            cleaned_sparql = response.content.replace("```", "")

            yield f"<code>{cleaned_sparql}</code>"
            yield '</br></br>SPARQL received. Querying DKG, please wait...</br></br>'

            try:
                result = dkg.graph.query(cleaned_sparql, repository="publicCurrent")
                yield f"<code>{result}</code>"
            except:
                yield "SPARQL query failed!"

            yield "</br></br><a href='javascript:history.back();'>[Go Back]</a>"

        return Response(stream_with_context(stream_results()))

    return render_template("form.html")


if __name__ == '__main__':
    app.run()
