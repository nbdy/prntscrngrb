# prntscrngrb
an image crawler/indexer for lightshot or prntscrn
## why?
idk. was bored<br>
don't even use it myself
## what does it do?
1. generate random string
2. append to prntscrn url
3. fetch image if not 404
5. save image to database
6. apply modules to entry
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

```
