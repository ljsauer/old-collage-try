# Old Collage Try 
### Apprenticeship capstone project, Feb. 2021
__________________
## Setup
> I recommend downloading [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) if you're not a venv expert. It makes the setup process a bit more straightforward, so I will assume that's how you're doing it in this README.
1. Clone the repo ([link for ssh cloning](git@github.com:ljsauer/old-collage-try.git))
2. Create a virtual environment using the PyCharm interface ([use this guide](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)). You will need Python installed already to do this (preferably >3.6).
3. With your virtual environment activated, install the packages in `requirements.txt`.
    >pip install -r requirements.txt
4. If you get errors pertaining to the `wordcloud` package, and are on Windows, you likely need to install the [C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), then try the above command again.
5. This next step is a bit weird and there's probably a better way to do it, but here's what you need to do:
   1. open a python shell in your virtual environment
   2. run `import nltk`
   3. then `nltk.download('punkt')`
   4. lastly `nltk.download('stopwords')`
   5. That will put the language dictionaries needed for the Natural Language Processing portion of the app in the proper places
6. From the root project directory, run `python main.py` and start uploading your own text files to make some ~art~!