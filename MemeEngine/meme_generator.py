from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    def __init__(self, output_dir: str):
        self._output_dir = Path.cwd().joinpath(Path(output_dir))

    def _load_image(self, img_location: Path) -> Image:
        return Image.open(img_location)

    def _save_image(self, image: Image, out_location: Path) -> Path:
        try:
            assert out_location.exists(), 'save location does not exist'
        except AssertionError as e:
            print("output directory doesn't exist ... creating ...")
            out_location.mkdir()
        try:
            image.save(out_location.joinpath('img.png'))
            return out_location.as_posix() + '/img.png'
        except OSError as e:
            print(f'Something went wrong when trying to write the image: {image} to disk: {self._output_dir}')
            print(e)

    def _resize_image(self, image: Image, width: int = 500) -> Image:
        current_width = image.width
        current_height = image.height
        aspect_ratio = current_width / current_height

        new_width = int(width)
        new_height = int(new_width * aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

        return resized_image

    def _write_on_image(self, image: Image, text: str) -> Image:
        # https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil#16377244
        draw_location: tuple = (0, 0)
        font_loc = Path(__file__).parents[1].joinpath('_data/fonts/BungeeSpice-Regular.ttf').as_posix()
        font = ImageFont.truetype(font_loc, size=24)
        ImageDraw.Draw(image).text(xy=draw_location, text=text, font=font, fill='black', align='center')

        return image

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        img_path = Path(img_path)
        image = self._load_image(img_location=img_path)
        resized_image = self._resize_image(image)
        quote = f'{text}\n    - {author}'
        image_with_quote = self._write_on_image(image=resized_image, text=quote)
        output = self._save_image(image=image_with_quote, out_location=self._output_dir)

        return output
