from flask import Flask, request, render_template, make_response, redirect, url_for
import bypasser
import re
import os

app = Flask(__name__)

ddllist = ['yadi.sk', 'disk.yandex.com', 'mediafire.com', 'uptobox.com', 'osdn.net', 'github.com',
           'hxfile.co', '1drv.ms', 'pixeldrain.com', 'antfiles.com', 'streamtape', 'racaty', '1fichier.com',
           'solidfiles.com', 'krakenfiles.com', 'mdisk.me', 'upload.ee', 'akmfiles', 'linkbox', 'shrdsk', 'letsupload.io',
           'zippyshare.com', 'wetransfer.com', 'we.tl', 'terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox',
           'teraboxapp', 'sbembed.com', 'watchsb.com', 'streamsb.net', 'sbplay.org', 'filepress',
           'fembed.net', 'fembed.com', 'femax20.com', 'fcdn.stream', 'feurl.com', 'layarkacaxxi.icu',
           'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'mm9842.com', 'anonfiles.com',
           'hotfile.io', 'bayfiles.com', 'megaupload.nz', 'letsupload.cc', 'filechan.org', 'myfile.is',
           'vshare.is', 'rapidshare.nu', 'lolabits.se', 'openload.cc', 'share-online.is', 'upvid.cc', ]

# Function to handle link bypassing
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
                temp = ddl.direct_link_generator(ele)
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

# Function to handle indexing
def handle_index(ele):
    result = bypasser.scrapeIndex(ele)
    # Here, you can implement how you want to handle the result
    # For example, you can store it in a variable or display it on the webpage.

# Main route to display the form and handle the link bypassing
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        result = loop_thread(url)

        # Get the current list of previously shortened links from the cookie
        prev_links_cookie = request.cookies.get('prev_links')
        prev_links = prev_links_cookie.split(',') if prev_links_cookie else []

        # If the result contains a valid link, add it to the list of previously shortened links
        if result and result.strip():
            prev_links.append(result.strip())

        # Limit the list of previously shortened links to a maximum of 10 (you can adjust this number)
        prev_links = prev_links[-10:]

        # Store the updated list of previously shortened links in a cookie
        response = make_response(render_template("index.html", result=result, prev_links=prev_links))
        response.set_cookie('prev_links', ','.join(prev_links))

        return response

    return render_template("index.html", result=None, prev_links=None)

if __name__ == "__main__":
    # Replace ddllist with your actual ddllist variable if it's defined somewhere in your code
    # You can set up your environment variables TOKEN, HASH, and ID for your application
    bot_token = os.environ.get("TOKEN", "")
    api_hash = os.environ.get("HASH", "")
    api_id = os.environ.get("ID", "")
    
    print("Web Application Starting")
    app.run()