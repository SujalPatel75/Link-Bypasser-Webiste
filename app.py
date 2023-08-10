from flask import Flask, request, render_template, make_response
import bypasser
import threading
import re
import os
from texts import gdrivetext, otherstext, ddltext, shortnertext, HELP_TEXT  
import pyrogram
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from os import environ, remove
from threading import Thread
from json import load
from re import search
from texts import HELP_TEXT
from ddl import ddllist, direct_link_generator
from time import time

app = Flask(__name__)

def handle_index(ele):
    result = bypasser.scrapeIndex(ele)


def store_shortened_links(link):
    with open('shortened_links.txt', 'a') as file:
        file.write(link + '\n')


def loop_thread(url):
    urls = []
    urls.append(url)

    if not url:
        return None

    link = ""
    for ele in urls:
        if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handle_index(ele)
            return
        elif bypasser.ispresent(ddllist, ele):
            try:
                temp = direct_link_generator(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        else:
            try:
                temp = bypasser.shortners(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        print("bypassed:", temp)
        if temp:
            link = link + temp + "\n\n"

    return link

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        result = loop_thread(url)

        resp = make_response(render_template("index.html", result=result))
        resp.set_cookie('shortened_links', result)

        return resp

    shortened_links = request.cookies.get('shortened_links')
    return render_template("index.html", result=None, shortened_links=shortened_links.split(",") if shortened_links else None)

if __name__ == "__main__":
    print("Web Application Starting")
    app.run()
