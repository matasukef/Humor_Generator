import os
import sys
import argparse
import flask
from flask import Flask, render_template, request, jsonify, Response
from werkzeug import secure_filename
import numpy as np
import base64
from chainer import serializers
import json
from PIL import Image

sys.path.append('..')
sys.path.append('../src/')
sys.path.append('../src/generator')
sys.path.append('../src/calc_sims/img_sim')
sys.path.append('../src/calc_sims/word_sim')
sys.path.append('../src/image_caption')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/CNN')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/generator')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/calc_sims/img_sim')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/calc_sims/word_sim')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/image_caption')

from HumorCaptionGenerator import HumorCaptionGenerator
from WEB_ENV import (
        UPLOAD_FOLDER,
        ALLOWED_EXTENSIONS,
        NUM_IMG_MULTIPLY,
    )

def model_configuration(args):
    
    #model configuration
    cnn_model_path = args.cnn_model_path
    cnn_model_type = args.cnn_model_type
    rnn_model_path = args.rnn_model_path
    word2vec_model_path = args.word2vec_model_path
    nic_dict_path = args.nic_dict_path
    class_table_path = args.class_table_path
    beamsize = args.beamsize
    depth_limit = args.depth_limit
    first_word = args.first_word
    hidden_dim = args.hidden_dim
    mean = args.mean
    feature = args.no_feature
    gpu = args.gpu

    conf_dict = {'cnn_model_path': cnn_model_path, 'cnn_model_type': cnn_model_type, 'rnn_model_path': rnn_model_path, 'word2vec_model_path': word2vec_model_path, 'nic_dict_path': nic_dict_path, 'class_table_path': class_table_path, 'beamsize': beamsize, 'depth_limit': depth_limit, 'first_word': first_word, 'hidden_dim': hidden_dim, 'mean': mean, 'feature': feature, 'gpu': gpu}

    return conf_dict

def allowed_file(filename):
    if '.' in filename and \
            filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

def agglutinative(tokens, agg=True):
    if agg:
        return ''.join(tokens)
    else:
        return ' '.join(tokens)

def parse_captions(captions, agg, beamsize):
    output = []
    for i, caption in enumerate(captions[:beamsize]):
        output.append({'No': i, 'caption': agglutinative(caption['sentence'][1:-1], agg), 'tokens': caption['sentence'], 'log': caption['log_likelihood'], 'num_tokens': len(caption['sentence'])})

    return output


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def generate_caption():
    title = 'Humor Caption Generator'
    conf = model_configuration(args)
    return render_template('index.html', title = title, configuration = conf)

@app.route('/api', methods=['POST'])
def return_captions():

    if request.method == 'POST':
        if request.mimetype== 'multipart/form-data':
            
            if 'file' in request.files:
                img = request.files['file']
                filename = secure_filename(img.filename)
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img.save(img_path)
            else:
                return 'error'

            if 'colloquial' in request.values:
                colloquial = True if request.values['colloquial'] == 'true' else False

            if 'num_caption' in request.values:
                num_caption = int(request.values['num_caption'])

            if 'offset' in request.values:
                offset = int(request.values['offset'])
            
            if 'img_sim' in request.values and 'word_sim' in request.values:
                img_sim = request.values['img_sim']
                word_sim = request.values['word_sim']
            else:
                return 'error'

    humor_captions = model.generate(
                        img = img_path,
                        multiple = 1,
                        num = num_caption,
                        cutoff = offset,
                        img_sim = img_sim,
                        word_sim = word_sim,
                        colloquial=colloquial
                    )

    print(humor_captions)
    return jsonify(humor_captions)

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--cnn_model_path', type=str, default=os.path.join('..', 'data', 'models', 'cnn', 'ResNet50.model'),
                        help="CNN model path")
    parser.add_argument('--cnn_model_type', type=str, default="ResNet", choices = ['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type used in NIC and img_sim")
    parser.add_argument('--rnn_model_path', type=str, default=os.path.join('..', 'data', 'models', 'rnn', 'STAIR_jp_256_Adam.model'),
                        help="RNN model path")
    parser.add_argument('--word2vec_model_path', type=str, default=os.path.join('..', 'data', 'word2vec', 'models', 'ja_wikipedia_neolog.model'),
                        help="word2vec model path")
    parser.add_argument('--nic_dict_path', type=str, default=os.path.join('..', 'data', 'nic_dict', 'dict_STAIR_jp_train.pkl'),
                        help="Neural image caption dictionary path")
    parser.add_argument('--class_table_path', type=str, default=os.path.join('..', 'data', 'wordnet', 'resnet_synsets_jp.txt'),
                        help="class table path")
    parser.add_argument('--beamsize', '-b', type=str, default=1,
                        help="beamsize")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50,
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--first_word', type=str, default='<S>',
                        help="first word")
    parser.add_argument('--hidden_dim', type=int, default=512,
                        help="dimension of hidden layeres")
    parser.add_argument('--mean', type=str, default='imagenet',
                        help="method to preprocess images")
    parser.add_argument('--no_feature', '-nf', action='store_false', 
                        help="use NIC feature when calculating img _sim")
    parser.add_argument('--gpu', '-g', type=int, default=0,
                        help="set GPU ID(negative value means using CPU)")
    args = parser.parse_args()


    model = HumorCaptionGenerator(
            rnn_model_path=args.rnn_model_path, #rnn model path used to generate caption
            cnn_model_path=args.cnn_model_path, #cnn model path to predict img sim and NIC 
            word2vec_model_path=args.word2vec_model_path, #word2vec model path for word sim
            nic_dict_path=args.nic_dict_path, #dictionary path used in NIC
            class_table_path=args.class_table_path, #class table path used in img sim
            cnn_model_type = args.cnn_model_type, #cnn type which is used in NIC and img_sim
            beamsize = int(args.beamsize), #num of generated captions
            depth_limit = int(args.depth_limit), # num of tokens in caption
            first_word=args.first_word, #first word used in NIC
            hidden_dim=args.hidden_dim, #hidden dim layers in NIC
            mean=args.mean, # method to preprocess images
            feature = args.no_feature, # use NIC feature or not when calc img_sim
            gpu_id = args.gpu # gpu id
        )

    configurations = model_configuration(args)
    
    app.run(debug=True)
