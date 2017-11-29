import os
import re
import argparse
import MeCab
from tqdm import tqdm

#delete () and [] 「」and so on
# separate all sentences in one line

def preprocess_wiki(input_dir, output_dir, no_end=True, cutoff=0, wakati=True, sep_line=True):

    reg = '</doc>'
    end = ['.', ',', '．', '，', '、', '。']
    to_end = str.maketrans(dict.fromkeys(end, ''))

    tagger = MeCab.Tagger('-Owakati')

    dirs = os.listdir(input_dir)
    for sub_dir in tqdm(dirs):
        sub_sub_dir = os.listdir(os.path.join(input_dir, sub_dir))
        
        for wiki_file in sub_sub_dir:
            articles = ''

            wiki_file_path = os.path.join(input_dir, sub_dir, wiki_file)

            with open(wiki_file_path, 'r') as f:
                article = f.read()

            article_list = re.split(reg, article)[:-1]
            
            for art in article_list:
                art = re.split('\n\n', art, maxsplit=1)[1]
                art = art.replace('\n', '').strip()
                
                if sep_line:
                    art.replace('.', '\n')
                    art.replace('。', '\n')

                if no_end:
                    art = art.translate(to_end)
                
                if len(art) >= cutoff:
                    if wakati:
                        art = tagger.parse(art)
                    
                    articles += art
                else:
                    pass

            sub_output_dir = os.path.join(output_dir, sub_dir)
            if not os.path.isdir(sub_output_dir):
                os.makedirs(sub_output_dir)

            output_file = os.path.join(sub_output_dir, wiki_file)
            
            with open(output_file, 'w') as f:
                f.write(articles)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', default=os.path.join('..', '..', '..', '..', 'data', 'word2vec', 'train_data', 'processed', 'wikipedia', 'ja_wikipedia'),
            help="input wikipedia dir")
    parser.add_argument('--output_dir', '-o', default=os.path.join('..', '..', '..', '..', 'data', 'word2vec', 'train_data', 'converted', 'wikipedia', 'ja_wikipedia_ipadic'),
            help="output wikipedia dir")
    parser.add_argument('--no_end', action='store_false',
            help="output file don't contain dots")
    parser.add_argument('--cutoff', '-c', type=int, default=100,
            help="cutoff to ignore article")
    parser.add_argument('--wakati', action='store_false',
            help="don't sepalate words")
    args = parser.parse_args()
    
    preprocess_wiki(args.input_dir, args.output_dir, args.no_end, args.cutoff, args.wakati)
