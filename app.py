import os
import asyncio

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")


async def generate_completion(i1, i2, i3):
    completion = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": generate_prompt(i1, i2, i3)},
        ]
    )
    return completion.choices[0].message.content


@app.route("/", methods=("GET", "POST"))
async def index():
    if request.method == "POST":
        i1, i2, i3 = request.form["interest1"], request.form["interest2"], request.form[
            "interest3"]
        result = await generate_completion(i1, i2, i3)
        return redirect(url_for("index", result=result))
    result = request.args.get("result")
    return await render_template("index.html", result=result)


def generate_prompt(i1, i2, i3):
    return f"""Comporta-te ca si cum ai fi expert in consultanta in cariera pentru 
    elevii de liceu. Iti voi da 3 interese pe care le am si tu trebuie sa imi recomanzi
    3 facultati din Romania. Raspunsul trebuie sa fie un tabel cu 3 coloane.
    Prima coloana sa fie numele facultatii impreuna cu universitatea din care 
    face parte, a doua coloana salariul mediu in Romania si
    a 3-a coloana 3 argumente pentru care crezi ca ar fi o alegere buna pentru mine sub
    forma de bullet points.

    Raspunsul trebuie sa fie strict in format HTML, sa-l putem afisa pe site. 
    Nimic altceva! 

    Acesta trebuie sa aiba borders si sa fie responsive. Fiecare coloana trebuie sa
    aiba padding de 5px.

    Interese:
     - {i1}
     - {i2}
     - {i3} 
     """
