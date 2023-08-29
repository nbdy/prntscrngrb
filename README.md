# prntscrngrb

an image crawler/indexer for lightshot/prntscrn

## what?

1. generate random string
2. append to prntscrn url
3. fetch image if not 404 
4. save image to database 
5. apply modules to entry

## modules
- [X] TextAnalyzer
  - Checks for text and saves it
- [X] NSFWAnalyzer
  - Detects nsfw and saves bounding boxes with label

## install

```shell
git clone https://github.com/nbdy/prntscrngrb
cd prntscrngrb
./dependencies.sh
pip3 install .
```

## use

```shell
usage: __main__.py [-h] [-l LANGUAGES [LANGUAGES ...]] [-d DIRECTORY] [-sl SUFFIX_LENGTH] [-co] [-db DATABASE] [--skip-indexing]

options:
  -h, --help            show this help message and exit
  -l LANGUAGES [LANGUAGES ...], --languages LANGUAGES [LANGUAGES ...]
                        TextDetector languages
  -d DIRECTORY, --directory DIRECTORY
                        Where to put them images
  -sl SUFFIX_LENGTH, --suffix_length SUFFIX_LENGTH
                        URL suffix length
  -co, --crawl-only     Only download images
  -db DATABASE, --database DATABASE
                        Database name
  --skip-indexing       Skip the indexing step
```
