#!bin/sh

python src/generator/HumorCaptionGenerator.py \
    --img 'sample_imgs/test.jpg' \
    --cnn_model_path 'data/models/cnn/ResNet50.model' \
    --cnn_model_type 'ResNet' \
    --rnn_model_path 'data/models/rnn/STAIR_jp_256_Adam.model' \
    --word2vec_model_path 'data/word2vec/models/ja_wikipedia_neolog.model' \
    --nic_dict_path 'data/nic_dict/dict_STAIR_jp_train.pkl' \
    --class_table_path 'data/wordnet/resnet_synsets_jp.txt' \
    --beamsize 1 \
    --depth_limit 50 \
    --first_word '<S>' \
    --hidden_dim 512 \
    --mean 'imagenet' \
    --img_multiply 5 \
    --output_size 10 \
    --cutoff 1 \
    --img_sim 'high' \
    --word_sim 'low' \
    --colloquial \
    --gpu 0
    #--no_feature \
