import logging
import os
import argparse
from gensim.models import word2vec

def train_word2vec(input_file, output_file, sg=0, size=200, window=5, min_count = 5, hs=0, negative = 5):

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    sg = 0 if sg == 'CBOW' else 1
    hs = 0 if hs == 'hierachical-softmax' else 1

    data = word2vec.LineSentence(input_file)
    model = word2vec.Word2Vec(data,
            sg = sg,
            size = size,
            window = window,
            min_count = min_count,
            hs = hs,
            negative = negative
        )
    model.save(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', '-i', type=str, default=os.path.join('..', '..', '..', '..', 'data', 'word2vec', 'train_data', 'training_data', 'ja_wikipedia.txt'),
                        help="intput file path which is separated sentences")
    parser.add_argument('--output_file', '-o', type=str, default=os.path.join('..', '..', '..', '..', 'data', 'word2vec', 'models', 'ja_wikipedia.model'),
                        help="output file path for word2vec model")
    parser.add_argument('--algorithm', '-a', type=str, default='CBOW', choices=['CBOW', 'skip-gram'],
                        help="type of training algorith CBOW or skip-gram")
    parser.add_argument('--size', type=int, default=200,
                        help="size of output vectors")
    parser.add_argument('--window', '-w', type=int, default=5,
                        help="number of window size")
    parser.add_argument('--min_count', '-mc', type=int, default=5,
                        help="cut off for word count")
    parser.add_argument('--hs', type=str, default='hierachical-softmax', choices=['hierachical-softmax', 'negative-sampling'],
                        help="type of output layer. hierachical-softmax or negative-sampling")
    parser.add_argument('--negative', '-n', type=int, default=5,
                        help="negative sampling")
    args = parser.parse_args()

    train_word2vec(input_file = args.input_file,
                   output_file = args.output_file,
                   sg = args.algorithm,
                   size = args.size,
                   window = args.window,
                   min_count = args.min_count,
                   hs = args.hs,
                   negative = args.negative
                   )
