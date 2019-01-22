# WikiChain

WikiChain is a simple Python script for generating nonsensical (and usually hilarious) essays for almost any topic using Wikipedia article content. 

### Installation:
```sh
$ pip3 install wikipedia markovify gevent
```

### Usage:
```sh
$ python wikichain.py <topic> [--depth 2] [--paragraphs 4] [--sentences 10]
```

### How does it work?

This script collects the text content of Wikipedia articles up to a certain search depth,
and then uses Markov chaining to string together vaguely human-understandable sentences. 

*Enjoy!*