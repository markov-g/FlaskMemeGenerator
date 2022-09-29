import os
import random
import argparse

import QuoteEngine as qe
import MemeEngine as me

def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(qe.ingestor.Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = qe.quote_model.QuoteModel(body, author)

    meme = me.meme_generator.MemeGenerator(img_location=img, output_dir='/tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


def make_parser():
    """Create an ArgumentParser for this script.

    :return: parser.
    """
    parser = argparse.ArgumentParser(
        description="Create a meme"
    )

    # Add arguments for custom data files.
    parser.add_argument('--body',
                        type=str,
                        help='a text quote body')
    parser.add_argument('--author',
                        type=str,
                        help='an text quote author')
    parser.add_argument('--path',
                        type=str,
                        help='a path of image directory')

    return parser

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    print(args)
    print(generate_meme(args.path, args.body, args.author))
