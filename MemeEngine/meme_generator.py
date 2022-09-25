from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
class MemeGenerator:
    def __init__(self, img_location: str, output_dir: str):
        img_path = Path(img_location)
        assert img_path.exists(), 'Image not found'

        self._image = self._load_image(img_location=img_path)
        self._output_dir = Path(output_dir)


    def _load_image(self, img_location: Path) -> Image:
        return Image.open(img_location)

    def _save_image(self, image: Image, out_location: Path) -> None:
        try:
            image.save(out_location)
        except OSError:
            print(f'Something went wrong when trying to write the image: {image} to disk: {self._output_dir}')

    def _resize_image(self, image: Image, width:int=500) -> Image:
        current_width = image.width
        current_height = image.height
        aspect_ratio = current_width / current_height

        new_width = width
        new_height = new_width * aspect_ratio

        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

        return resized_image

    def _write_on_image(self, image: Image, text: str) -> Image:
        # https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil#16377244
        draw_location: tuple = (0, 0)
        font = ImageFont.truetype("sans-serif.ttf", 20)
        ImageDraw.Draw(image).text(xy=draw_location, text=text, font=font)

        return image

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        resized_image = self._resize_image(self._image)
        quote = f'{text}\n    - {author}'
        image_with_quote = self._write_on_image(image=resized_image, text=quote)
        self._save_image(image=image_with_quote, out_location=self._output_dir)

        return self._output_dir
