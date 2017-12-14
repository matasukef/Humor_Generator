import os
import sys
import argparse
from tqdm import tqdm

sys.path.append('../../src/calc_sims/img_sim')
sys.path.append('../../src/calc_sims/word_sim')
sys.path.append('../../src/image_caption')
sys.path.append('../../src/generator')
sys.path.append('../../src/')

from generator.HumorCaptionGenerator import HumorCaptionGenerator

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', '-i', type=str, default=os.path.join('..', 'static', 'images', 'mpii_human_pose'), help="input image")
    parser.add_argument('--output_csv_dir', type=str,
                        default=os.path.join('..', 'static', 'data'))
    parser.add_argument('--experiment1', type=str, default='experiment1.csv')
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', '..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--rnn_model_path', type=str, default=os.path.join('..', '..', 'data', 'models', 'rnn', 'STAIR_jp_256_Adam.model'),
                        help="RNN model path")
    parser.add_argument('--word2vec_model_path', type=str, default=os.path.join('..', '..', 'data', 'word2vec', 'models', 'ja_wikipedia_neolog.model'),
                        help="Word2vec model path")
    parser.add_argument('--nic_dict_path', type=str, default=os.path.join('..', '..', 'data', 'nic_dict', 'dict_STAIR_jp_train.pkl'),
                        help="Neural image caption dictionary path")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', '..', 'data', 'wordnet', 'resnet_synsets_jp_modified.txt'),
                        help="class table path")
    parser.add_argument('--beamsize', '-b', type=int, default=1,
                        help="beamsize of neural image caption")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50,
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--first_word', type=str, default='<S>',
                        help="first word")
    parser.add_argument('--hidden_dim', type=int, default=512,
                        help="dimension of hidden layers")
    parser.add_argument('--mean', type=str, default="imagenet",
                        help="method to preprocess images")
    parser.add_argument('--no_feature', '-f', action='store_false',
                        help="don't use image features to calc img sim class")
    parser.add_argument('--img_multiply', '-mt', type=int, default=5,
                        help="multiply by num size of image classes is generated")
    parser.add_argument('--output_size', type=int, default=50,
                        help="output size")
    parser.add_argument('--cutoff', '-c', type=int, default=1,
                        help="the number of ignoring top n img sim word")
    parser.add_argument('--colloquial', '-co', action='store_true',
                        help="return captions as colloquial")
    parser.add_argument('--gpu', '-g', type=int, default=0,
                        help="GPU ID (put -1 if you don't use gpu)")

    args = parser.parse_args()

    model = HumorCaptionGenerator(
        rnn_model_path=args.rnn_model_path,
        cnn_model_path=args.cnn_model_path,
        word2vec_model_path=args.word2vec_model_path,
        nic_dict_path=args.nic_dict_path,
        class_table_path=args.class_table_path,
        cnn_model_type=args.cnn_model_type,
        beamsize=args.beamsize,
        depth_limit=args.depth_limit,
        first_word=args.first_word,
        hidden_dim=args.hidden_dim,
        mean=args.mean,
        feature=args.no_feature,
        gpu_id=args.gpu
    )

    images = os.listdir(args.img_dir)

    # experiment
    experiment1_path = os.path.join(args.output_csv_dir, args.experiment1)
    experiment1_header = 'no,images,cap_original,cap_ll,cap_lh,cap_hl,cap_hh' + '\n' 

    # write experiment1 header
    with open(experiment1_path, 'w') as f:
        f.write(experiment1_header)

    for i, image in tqdm(enumerate(images)):
        img_path = os.path.join(args.img_dir, image)

        print(img_path)

        print('result_ll')

        result_ll = model.generate(img=img_path,
                                   multiple=args.img_multiply,
                                   num=args.output_size,
                                   cutoff=0,
                                   img_sim='low',
                                   word_sim='low',
                                   colloquial=True
                                   )

        print('result_lh')
        result_lh = model.generate(img=img_path,
                                   multiple=args.img_multiply,
                                   num=args.output_size,
                                   cutoff=0,
                                   img_sim='low',
                                   word_sim='high',
                                   colloquial=True
                                   )

        print('result_hl')
        result_hl = model.generate(img=img_path,
                                   multiple=args.img_multiply,
                                   num=args.output_size,
                                   cutoff=args.cutoff,
                                   img_sim='high',
                                   word_sim='low',
                                   colloquial=True
                                   )

        print('result_hh')
        result_hh = model.generate(img=img_path,
                                   multiple=args.img_multiply,
                                   num=args.output_size,
                                   cutoff=0,
                                   img_sim='high',
                                   word_sim='high',
                                   colloquial=True
                                   )

        caption = result_hl[0]['caption']['sentence']
        cap_ll = result_ll[0]['humor_captions']
        cap_lh = result_lh[0]['humor_captions']
        cap_hl = result_hl[0]['humor_captions']
        cap_hh = result_hh[0]['humor_captions']

        result = model.generate(
            img=img_path,
            multiple=args.img_multiply,
            num=args.output_size,
            cutoff=args.cutoff,
            img_sim='high',
            word_sim='low',
            colloquial=True
        )

        caption = result[0]['caption']['sentence']
        humor_caption = result[0]['humor_captions']

        if '<UNK>' in caption:
            continue
        elif not cap_ll or not cap_lm or not cap_lh \
                or not cap_ml or not cap_mm or not cap_mh \
                or not cap_hl or not cap_hm or not cap_hh:
            continue

        body = str(i + 1) + ',' + image + ','

        # experiment1
        exp1_body = body + caption + ',' + cap_hl[0] + '\n'

        with open(experiment1_path, 'a') as f:
            f.write(exp1_body)

        # experiment2
        exp2_body = body + cap_ll[0] + ',' + cap_lm[0] + ',' + cap_lh[0] + ',' + \
            cap_ml[0] + ',' + cap_mm[0] + ',' + cap_mh[0] + ',' + \
            cap_hl[0] + ',' + cap_hm[0] + ',' + cap_hh[0] + '\n'

        with open(experiment2_path, 'a') as f:
            f.write(exp2_body)

        # experiment3
        exp3_body = body + cap_hl[0] + '\n'

        with open(experiment3_path, 'a') as f:
            f.write(exp3_body)
