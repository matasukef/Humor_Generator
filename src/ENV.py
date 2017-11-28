import os

#alexnet and vgg16 are not prepared yet.

current_dir = os.path.dirname(os.path.abspath(__file__))

#model path
MODEL_RESNET = os.path.join(current_dir, '..', 'data', 'models', 'cnn', 'ResNet50.model')
MODEL_VGG16 = os.path.join(current_dir, '..', 'data', 'models', 'cnn', 'VGG16.model')
MODEL_ALEXNET = os.path.join(current_dir, '..', 'data', 'models', 'cnn', 'AlexNet.model')

#vocab path
NORM_LIST_EN = os.path.join(current_dir, '..', 'data', 'wordnet', 'resnet_synsets.txt')
NORM_LIST_JP = os.path.join(current_dir, '..', 'data', 'wordnet', 'resnet_synsets_jp.txt')

#caption vocab
CAP_VOCAB_JP = os.path.join(current_dir, '..', 'data', 'nic_dict', 'dict_STAIR_jp_train.pkl')
CAP_VOCAB_EN = os.path.join(current_dir, '..', 'data', 'nic_dict', 'dict_MSCOCO_en_train.pkl')
CAP_VOCAB_CH = os.path.join(current_dir, '..', 'data', 'nic_dict', 'dcit_MSCOCO_ch_mt_train.pkl')

#caption rnn_model
CAP_RNN_MODEL_JP = os.path.join(current_dir, '..', 'data', 'models', 'rnn', 'STAIR_jp_256_Adam.model')
CAP_RNN_MODEL_EN = os.path.join(current_dir, '..', 'data', 'models', 'rnn', 'MSCOCO_en_256_Adam.model')
CAP_RNN_MODEL_CH = os.path.join(current_dir,  '..', 'data', 'models', 'rnn', 'MSCOCO_ch_mt_256_Adam.model')

#wordnet database
WORDNET_DATABASE = os.path.join(current_dir, '..', 'data', 'wordnet', 'wnjpn.db')

#dataset for word2vec
NEOLOG_DIC = os.path.join('/', 'usr', 'lib', 'mecab', 'dic', 'mecab-ipadic-neologd')

#word2vec
W2V_WIKIPEDIA = os.path.join(current_dir, '..', 'data', 'word2vec_dict', 'entity_vector', 'entity_vector.model.bin')
