import sys
import os
import sqlite3
from tqdm import tqdm
import argparse

sys.path.append('..')
from ENV import WORDNET_DATABASE, WORDS_RESNET

def make_hype_list(obj_list, db, lang):
    result = ''
    conn = sqlite3.connect(db)

    with open(obj_list, 'r') as f:
        synset = f.read().split('\n')[:-1]

    synset_id = [obj.split()[0] for obj in synset]
    synset_obj = [obj.split()[1].split(',')[0] for obj in synset]

    for word_id, word_obj in tqdm(zip(synset_id, synset_obj)):
        sql = 'select lemma from synlink, sense, word where link ="hype" and synset1 = ? and synset2 = synset and sense.wordid = word.wordid and word.lang= ?'
        synset = (word_id[1:] + '-n', lang)
        cur = conn.execute(sql, synset)
        row = cur.fetchone()

        result += word_id + ' ' + row[0] + '\n'

    return result


if __name__ == '__main__':
    parser =argparse.ArgumentParser()
    parser.add_argument('--input_path', '-i', type=str, default=WORDS_RESNET,
                        help="inputfile path")
    parser.add_argument('--database', '-db', type=str, default=WORDNET_DATABASE,
                        help="wordnet database path")
    parser.add_argument('--output_path', '-op', type=str, default=os.path.join('..', '..', 'data', 'vocab', 'hype_list.txt'),
                        help="outputfile path")
    parser.add_argument('--lang', '-l', type=str, default='eng', choices=['eng', 'jpn'],
                        help="language to be replaced")
    args = parser.parse_args()

    result = make_hype_list(args.input_path, args.database, args.lang)

    with open(args.output_path, 'w') as f:
        f.write(result)
