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

sys.path.append('../src/generator')
sys.path.append('../src/calc_sims/img_sim')
sys.path.append('../src/calc_sims/word_sim')
sys.path.append('../src/image_caption')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/CNN')
sys.path.append('..')
from HumorCaptionGenerator import HumorCaptionGenerator
from WEB_ENV import (
        UPLOAD_FOLDER,
        ALLOWED_EXTENSIONS,
        NUM_IMG_MULTIPLY,
    )

def model_configuration(args):
    
    lang = args.lang
    #model configuration
    #cnn_model_path = args.cnn_model_path
    cnn_model_type = args.cnn_model_type
    beamsize = args.beamsize
    word_dict = args.word_dict
    depth_limit = args.depth_limit
    gpu = args.gpu

    conf_dict = {'lang': lang, 'cnn_model_type': cnn_model_type, 'beamsize': beamsize, 'depth_limit': depth_limit, 'gpu': gpu, 'word_dict': word_dict}

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

    print(request.values)
    humor_captions = model.generate(
                        img = img_path,
                        multiple = NUM_IMG_MULTIPLY,
                        num = num_caption,
                        cutoff = offset,
                        img_sim = img_sim,
                        word_sim = word_sim,
                        colloquial=colloquial
                    )

    return jsonify(humor_captions)

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l', type=str, default='jp', choices = ['jp', 'en', 'ch'],
                        help="choose language to generate captions and output image class")
    parser.add_argument('--cnn_model_type', '-ct', type=str, default="ResNet", choices = ['ResNet', 'VGG16', 'AlexNet'],
                        help="CNN model type used in NIC and img_sim")
    parser.add_argument('--beamsize', '-b', type=str, default=1,
                        help="beamsize")
    parser.add_argument('--word_dict', '-wd', type=str, default='jp_wiki_neolog', choices = ['jp_wiki_neolog', 'jp_wiki_ipadic'],
                        help="word2vec dictionary")
    parser.add_argument('--depth_limit', '-dl', type=int, default=50,
                        help="max limit of generating tokens when constructing captions")
    parser.add_argument('--no_feature', '-nf', action='store_false', 
                        help="use NIC feature when calculating img _sim")
    parser.add_argument('--gpu', '-g', type=int, default=0,
                        help="set GPU ID(negative value means using CPU)")
    #parser.add_argument('--rnn_model_path', '-rm', type=str)
    #parser.add_argument('--cnn_model_path', '-rm', type=str)
    #parser.add_argument('--nic_dict_path', '-rm', type=str)
    #parser.add_argument('--word_sim_model_path', '-rm', type=str)
    args = parser.parse_args()


    model = HumorCaptionGenerator(
            lang = args.lang, #same with rnn model type
            cnn_model_type = args.cnn_model_type, #cnn type which is used in NIC and img_sim
            beamsize = args.beamsize, #num of generated captions
            depth_limit = args.depth_limit, # num of tokens in caption
            word_dict = args.word_dict, #word dict type used in word_sim
            feature = args.no_feature, # use NIC feature or not when calc img_sim
            gpu_id = args.gpu # gpu id
        )

    configurations = model_configuration(args)
    
    app.run(debug=True)
