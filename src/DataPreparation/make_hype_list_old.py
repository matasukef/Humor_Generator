import sys
import os
import sqlite3
from tqdm import tqdm
import argparse

sys.path.append('..')
from ENV import WORDNET_DATABASE, WORDS_RESNET

def split_synset(obj_list):

    with open(obj_list, 'r') as f:
        synset = f.read().split('\n')[:-1]

    if '->' in synset[0].split()[0]:
        synset_id = [obj.split()[0].split('->')[1] for obj in synset ]
    else:
        synset_id = [obj.split()[0] for obj in synset]
    
    synset_obj = [obj.split()[1].split(',')[0] for obj in synset]

    return synset_id, synset_obj

def make_hype_list(obj_list, db, lang):
    result = ''
    conn = sqlite3.connect(db)

    synset_id, synset_obj = split_synset(obj_list)

    for word_id, word_obj in tqdm(zip(synset_id, synset_obj)):
        sql = 'select synset2, lemma from synlink, sense, word where link ="hype" and synset1 = ? and synset2 = synset and sense.wordid = word.wordid and word.lang= ?'
        synset = (word_id[1:] + '-n', lang)
        cur = conn.execute(sql, synset)
        row = cur.fetchone()

        result += word_id + '->' + 'n' + row[0][:-2] + ' ' + row[1] + '\n'

    return result


def translate_to_japanese(obj_list, db):
    result = ''
    conn = sqlite3.connect(db)

    synset_id, synset_obj = split_synset(obj_list)
    
    for word_id, word_obj in tqdm(zip(synset_id, synset_obj)):
        sql = 'select lemma from sense, word where synset = ? and sense.wordid = word.wordid and word.lang="jpn"'
        synset = (word_id[1:] + '-n', )
        cur = conn.execute(sql, synset)
        row = cur.fetchall()

        if not row:
            word_id = word_id[1:] + '-n'
            while not row:
                hype_word_id = get_hype(word_id, conn)
                row = get_translated(hype_word_id, conn)
                if not row:
                    word_id = hype_word_id
        
        result += word_id + ' '
        for r in row:
            if r != row[-1]:
                result += r[0] + ', '
            else:
                result += r[0] + '\n'

    return result
        
''' 
        if row:
            result += word_id + ' '
            for r in row:
                if r != row[-1]:
                    result += r[0] + ', '
                else:
                    result += r[0] + '\n'

        else:
            word_id = word_id[1:] + '-n'
            while not row:
                hype_word_id = get_hype(word_id, conn)
                row = get_translated(hype_word_id, conn)
                word_id = hype_word_id
            
            result += word_id + ' '
            for r in row:
                if r != row[-1]:
                    result += r[0] + ', '
                else:
                    result += r[0] + '\n'
            #result += word_id + ' ' + word_obj + '\n'

    return result
'''

def get_hype(synset_id, conn):
    sql = 'select synset2 from synlink, sense, word where link="hype" and synset1 = ? and synset2 = synset and sense.wordid = word.wordid and word.lang="eng"'
    synset = (synset_id, )
    cur = conn.execute(sql, synset)
    row = cur.fetchone()

    return row[0]

def get_translated(synset_id, conn):
    sql = 'select lemma from sense, word where synset = ? and sense.wordid = word.wordid and word.lang="jpn"'
    synset = (synset_id, )
    cur = conn.execute(sql, synset)
    row = cur.fetchall()

    return row

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
    parser.add_argument('--type', type=str, default='hype', choices= ['hype', 'translate'],
                        help="choose type to execute (get hype or translate)")
    args = parser.parse_args()

    if args.type == 'hype':
        result = make_hype_list(args.input_path, args.database, args.lang)
    else:
        result = translate_to_japanese(args.input_path, args.database)

    with open(args.output_path, 'w') as f:
        f.write(result)
