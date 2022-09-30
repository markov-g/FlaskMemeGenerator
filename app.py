import random
import os
from typing import Optional
import requests
from requests import RequestException
import tempfile
from pathlib import Path
from flask import Flask, render_template, abort, request

import QuoteEngine as qe
import MemeEngine as me

app = Flask(__name__)
meme = me.meme_generator.MemeGenerator(output_dir='static')

def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(qe.ingestor.Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()

@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    meme_path = meme.make_meme(img, quote.body, quote.author)

    return render_template('meme.html', path=get_relative_path(meme_path))


def get_relative_path(img_path: Path, proj_path: Path = Path(__file__).parent) -> Path:
    return Path(img_path).relative_to(proj_path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    image_url_id = 'image_url'
    quote_body_id = 'body'
    quote_author_id = 'author'

    img = download_image(image_url=request.form.get(image_url_id))
    if img == None:
        return render_template('meme_form.html', error="some went wrong, when trzing to download the image")
    else:
        meme_path = meme.make_meme(img,
                              request.form.get(quote_body_id),
                              request.form.get(quote_author_id)
                              )


        return render_template('meme.html', path=get_relative_path(meme_path))

def download_image(image_url: str) -> Optional[str]:
    # https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c
    filename = image_url.split("/")[-1]
    download_location = Path(tempfile.gettempdir(), f"{filename}")
    try:
        img_req = requests.get(image_url, stream = True)
        if img_req.status_code == 200:
            with open(download_location, 'wb') as img_f:
                img_f.write(img_req.content)
                return str(download_location)

    except request.ConnectionError:
        return None
    except RequestException:
        return None


if __name__ == "__main__":
    app.run()
