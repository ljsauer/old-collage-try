import os


class Settings:
    collage_dir: str = f"{os.getcwd()}/static"
    object_image_path: str = f"{os.getcwd()}/static"
    n_words: int = 15    # number of important words from text to include in collage
    n_sentences: int = 10   # not used in this project currently
    image_per_word: int = 5   # number of images to represent each word in collage
    image_width: int = 1024   # width of the image collage
    image_height: int = 768   # height of the image collage
    max_object_size: int = int(image_width * .2)
