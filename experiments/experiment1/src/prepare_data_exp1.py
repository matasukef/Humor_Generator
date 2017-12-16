import os
import sys
import argparse
from tqdm import tqdm

sys.path.append('../../../src/calc_sims/img_sim')
sys.path.append('../../../src/calc_sims/word_sim')
sys.path.append('../../../src/image_caption')
sys.path.append('../../../src/generator')
sys.path.append('../../../src/')

from generator.HumorCaptionGenerator import HumorCaptionGenerator


def get_top_sim_score(sim_words, word):
    for sim in sim_words:
        if sim['norm'] == word:
            return sim['sim']


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--img_dir', '-i', type=str, default=os.path.join(
        '..', 'static', 'images', 'human_images'), help="input image")
    parser.add_argument('--output_csv_dir', type=str,
                        default=os.path.join('..', 'static', 'data'))
    parser.add_argument('--experiment1', type=str, default='experiment1.csv')
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', '..', '..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', type=str, default='ResNet', choices=['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type")
    parser.add_argument('--rnn_model_path', type=str, default=os.path.join('..', '..', '..', 'data', 'models', 'rnn', 'STAIR_jp_256_Adam.model'),
                        help="RNN model path")
    parser.add_argument('--word2vec_model_path', type=str, default=os.path.join('..', '..', '..', 'data', 'word2vec', 'models', 'ja_wikipedia_neolog.model'),
                        help="Word2vec model path")
    parser.add_argument('--word2vec_binary_data', action="store_true",
                        help="use binary data for word2vec model")
    parser.add_argument('--nic_dict_path', type=str, default=os.path.join('..', '..', '..', 'data', 'nic_dict', 'dict_STAIR_jp_train.pkl'),
                        help="Neural image caption dictionary path")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', '..', '..', 'data', 'wordnet', 'resnet_synsets_jp_modified.txt'),
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
    parser.add_argument('--cutoff', '-c', type=int, default=0,
                        help="the number of ignoring top n img sim word")
    parser.add_argument('--colloquial', '-co', action='store_false',
                        help="return captions as colloquial")
    parser.add_argument('--gpu', '-g', type=int, default=0,
                        help="GPU ID (put -1 if you don't use gpu)")

    args = parser.parse_args()

    model = HumorCaptionGenerator(
        rnn_model_path=args.rnn_model_path,
        cnn_model_path=args.cnn_model_path,
        word2vec_model_path=args.word2vec_model_path,
        word2vec_binary_data=args.word2vec_binary_data,
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
    experiment1_header = 'no,images,subject,cap_original,cap_ll,cap_lh,cap_hl,cap_hh,' + \
                         'll_humor_score,ll_img_sim,ll_word_sim,'+ \
                         'lh_humor_score,lh_img_sim,lh_word_sim,' + \
                         'hl_humor_score,hl_img_sim,hl_word_sim,' + \
                         'hh_humor_score,hh_img_sim,hh_word_sim' + '\n'


    # write experiment1 header
    with open(experiment1_path, 'w') as f:
        f.write(experiment1_header)

    for i, image in tqdm(enumerate(images)):
        img_path = os.path.join(args.img_dir, image)


        result_ll = model.generate(img=img_path,
                                   num=args.output_size,
                                   cutoff=0,
                                   img_sim='low',
                                   word_sim='low',
                                   colloquial=args.colloquial
                                   )

        result_lh = model.generate(img=img_path,
                                   num=args.output_size,
                                   cutoff=0,
                                   img_sim='low',
                                   word_sim='high',
                                   colloquial=args.colloquial
                                   )

        result_hl = model.generate(img=img_path,
                                   num=args.output_size,
                                   cutoff=args.cutoff,
                                   img_sim='high',
                                   word_sim='low',
                                   colloquial=args.colloquial
                                   )

        result_hh = model.generate(img=img_path,
                                   num=args.output_size,
                                   cutoff=0,
                                   img_sim='high',
                                   word_sim='high',
                                   colloquial=args.colloquial
                                   )

        caption = result_hl[0]['caption']['sentence']
        cap_ll = result_ll[0]['humor_captions']
        cap_lh = result_lh[0]['humor_captions']
        cap_hl = result_hl[0]['humor_captions']
        cap_hh = result_hh[0]['humor_captions']

        if '<UNK>' in caption:
            continue
        elif not cap_ll or not cap_lh or not cap_hl or not cap_hh:
            continue
        elif caption in (cap_ll[0], cap_lh[0], cap_hl[0], cap_hh[0]):
            print("origin")
            continue
        elif cap_ll[0] in (caption, cap_lh[0], cap_hl[0], cap_hh[0]):
            print("capll")
            continue
        elif cap_lh[0] in (caption, cap_ll[0], cap_hl[0], cap_hh[0]):
            print("caplh")
            continue
        elif cap_hl[0] in (caption, cap_ll[0], cap_lh[0], cap_hh[0]):
            print("cap_hl")
            continue
        elif cap_hh[0] in (caption, cap_ll[0], cap_lh[0], cap_hl[0]):
            print("caphh")
            continue


        print(image)
        # similariy
        ll_humor_score = result_ll[0]['img_word_sim_words'][0]['score']
        ll_humor_norm = result_ll[0]['img_word_sim_words'][0]['norm']
        ll_img_sim_words = result_ll[0]['img_sim_words']
        ll_word_sim_words = result_ll[0]['word_sim_words']
        ll_img_sim = get_top_sim_score(ll_img_sim_words, ll_humor_norm)
        ll_word_sim = get_top_sim_score(ll_word_sim_words, ll_humor_norm)

        lh_humor_score = result_lh[0]['img_word_sim_words'][0]['score']
        lh_humor_norm = result_lh[0]['img_word_sim_words'][0]['norm']
        lh_img_sim_words = result_lh[0]['img_sim_words']
        lh_word_sim_words = result_lh[0]['word_sim_words']
        lh_img_sim = get_top_sim_score(lh_img_sim_words, lh_humor_norm)
        lh_word_sim = get_top_sim_score(lh_word_sim_words, lh_humor_norm)

        hl_humor_score = result_hl[0]['img_word_sim_words'][0]['score']
        hl_humor_norm = result_hl[0]['img_word_sim_words'][0]['norm']
        hl_img_sim_words = result_hl[0]['img_sim_words']
        hl_word_sim_words = result_hl[0]['word_sim_words']
        hl_img_sim = get_top_sim_score(hl_img_sim_words, hl_humor_norm)
        hl_word_sim = get_top_sim_score(hl_word_sim_words, hl_humor_norm)

        hh_humor_score = result_hh[0]['img_word_sim_words'][0]['score']
        hh_humor_norm = result_hh[0]['img_word_sim_words'][0]['norm']
        hh_img_sim_words = result_hh[0]['img_sim_words']
        hh_word_sim_words = result_hh[0]['word_sim_words']
        hh_img_sim = get_top_sim_score(hh_img_sim_words, hh_humor_norm)
        hh_word_sim = get_top_sim_score(hh_word_sim_words, hh_humor_norm)

        body = str(i + 1) + ',' + image + ',' + result_hl[0]['subject'] + ','

        # experiment1
        exp1_body = body + caption + ',' + cap_ll[0] + ',' + \
                cap_lh[0] + ',' + cap_hl[0] + ',' + cap_hh[0] + ',' + \
            str(ll_humor_score) + ',' + str(ll_img_sim) + ',' + str(ll_word_sim) + ',' + \
            str(lh_humor_score) + ',' + str(lh_img_sim) + ',' + str(lh_word_sim) + ',' + \
            str(hl_humor_score) + ',' + str(hl_img_sim) + ',' + str(hl_word_sim) + ',' + \
            str(hh_humor_score) + ',' + str(hh_img_sim) + ',' + str(hh_word_sim) + '\n'

        with open(experiment1_path, 'a') as f:
            f.write(exp1_body)
