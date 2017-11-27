#!bin/sh

cd src/word_sim
git clone https://github.com/attardi/wikiextractor
cd ../..
python src/word_sim/wikiextractor/WikiExtractor.py jawiki-latest-pages-articles.xml.bz2 --output data/word2vec/

cat text/*/* > jawiki.txt
