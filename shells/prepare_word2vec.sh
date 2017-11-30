#!bin/sh


#japanese wikipedia
git clone https://github.com/attardi/wikiextractor src/calc_sim/word_sim/train

python src/calc_sim/word_sim/wikiextractor/WikiExtractor.py --output data/word2vec/train_data/processed/wikipedia/ja_wikipedia data/word2vec/train_data/original/wikipedia/jawiki-latest-pages-articles.xml.bz2

python src/calc_sims/word_sim/train/preprocess_wiki.py \
    --intput_dir data/word2vec/train_data/processed/wikipedia/ja_wikipedia
    --output_dir data/word2vec/train_data/converted/wikipedia/ja_wikipedia
    --cutoff 100

cat data/word2vec/train_data/converted/ja_wikipedia/*/* > data/word2vec/train_data/training_data/jawiki.txt

