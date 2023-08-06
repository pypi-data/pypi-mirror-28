# srp_nlp
> Natural language processing with Python for SRP peeps :metal:

A lot of this stuff can be reused in other projects, so I figured I'd just let it live here, that way we can clone and reuse as needed.

In this repo you'll find two main repos:
+ **code**: This is just a couple of `.py` files, one for each class.
+ **notebooks**: This has tutorials in the form of jupyter notebooks.

## Getting Started
So you don't mess up your python environment, you should create a new one, install required libraries, and then run everything.
Here's how to do that using `conda` (assuming you want to name your environment 'nlp'):

```
>> conda create --name nlp python=2.7 
# (type 'y' when prompted)
>> source activate nlp
>> git clone ________
>> cd ______
>> conda install requirements.txt
```

Note -if you don't already have `nltk` already installed, you'll need to download the nltk stuff. 
Just type the following into your shell:

```
>> python
>> import nltk
>> nltk.download()
# click download when prompted
```


## Implemented Classes
+ `TextProcessor()`:
+ `BagofWords()`:
+ `TF-IDF()`:


## Usage Examples
Most of the methods have (or will have) examples in the `notebooks`. Just find the corresponding notebook.

Here's some brief examples anyway:

### TextProcessor

```
from Preprocessing import TextProcessor
textCleaner = TextProcessor()
textCleaner.fit(data)
cleaned_data = textCleaner.transform(data)
```


## Author
+ [github/https://github.com/jwilber](https://github.com/jwilber)

## License.
Released under the GNU license

***


