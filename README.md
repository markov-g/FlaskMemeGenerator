# FlaskMemeGenerator
A simple Flask-based application that can be used to generate memes using customizable image and quote input.


![meme_exmaple](./static/img.png)


# Requirements
To run, you need to have 
1. `python` >= 3.8  
2. `pipenv` and 
3. `pdftotext` CLI utility provided via `xpdf`
installed.

Note: For users of `NixOS` or the `nixpkgs`, you can use the `shell.nix` from this directory to install all dependencies:
```bash
nix-shell shell.nix
```

Once the 3 dependencies have been installed, to set-up a virtual environment with all library dependencies (specified in the Pipfile), ensure `python` and `pipenv` are in your PATH and run:
```bash
cd MemeGenerator
pipenv --python `which python` --bare install
```

After the environment has been set-up, you can run the application via:
### 1. CLI
```bash
pipenv run python meme.py --help
```

or 
### 2. Flask 
```bash
export FLASK_APP=app
export FLASK_ENV=development
pipenv run python flask run
```

## Modules
### Quote engine
The `QuoteEngine` module is responsible for ingesting different types of files that contain quotes. The Ingestor class can read different kinds of file formats such as 'csv', 'docx', 'pdf', and 'txt'.
It expects the following format: `"This is quote body" - author`. The module implements the strategy pattern to allow some flexibility in the supported quote formats. 

### Meme engine
The `MemeEngine` module is responsible for manipulating and drawing text onto images. It uses the `pillow` library.