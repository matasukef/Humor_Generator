import os

current_dir = os.path.dirname(os.path.abspath(__file__))

#model path
MODEL_RESNET = os.path.join(current_dir, '..', 'data', 'models', 'cnn', 'ResNet50.model')
MODEL_VGG16 = os.path.join(current_dir, '..', 'data', 'models', 'cnn', 'VGG16.model')
MODEL_ALEXNET = os.path.join(current_dir, '..', 'data', 'models', 'cnn', 'AlexNet.model')

#vocab path
WORDS_RESNET = os.path.join(current_dir, '..', 'data', 'vocab', 'resnet_synsets.txt')
WORDS_VGG16 = os.path.join(current_dir, '..', 'data', 'vocab', 'vgg16_synsets.txt')
WORDS_ALEXNET = os.path.join(current_dir, '..', 'data', 'vocab', 'alexnet_synsets.txt')

#caption vocab
CAP_VOCAB_JP = os.path.join(current_dir, '..', 'data', 'vocab_dict', 'dict_STAIR_jp_train.pkl')
CAP_VOCAB_EN = os.path.join(current_dir, '..', 'data', 'vocab_dict', 'dict_MSCOCO_en_train.pkl')
CAP_VOCAB_CH = os.path.join(current_dir, '..', 'data', 'vocab_dict', 'dcit_MSCOCO_ch_mt_train.pkl')

#caption rnn_model
CAP_RNN_MODEL_JP = os.path.join(current_dir, '..', 'data', 'models', 'rnn', 'STAIR_jp_256_Adam.model')
CAP_RNN_MODEL_EN = os.path.join(current_dir, '..', 'data', 'models', 'rnn', 'MSCOCO_en_256_Adam.model')
CAP_RNN_MODEL_CH = os.path.join(current_dir,  '..', 'data', 'models', 'rnn', 'MSCOCO_ch_mt_256_Adam.model')

#wordnet database
WORDNET_DATABASE = os.path.join(current_dir, '..', 'data', 'vocab', 'wnjpn.db')
