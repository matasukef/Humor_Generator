#!bin/sh

return_yes_or_no(){

    _ANSWER=

    while :
    do
        if [ "`echo -n`" = "-n" ]; then
            echo "$@\c"
        else
            echo -n "$@"
        fi
        read _ANSWER
        case "$_ANSWER" in
            [yY] | yes | YES | Yes) return 0 ;;
            [nN] | no | NO | No ) return 1 ;;
            * ) echo "type yes or no."
        esac
    done
}

echo 'Do you want to download pre-trained models? (yes/no): '
models_download=`return_yes_or_no`

if $models_download ; then


    if [ ! -d data/models/cnn ]; then
        mkdir --parents data/models/cnn
        echo 'Downloading pre-trained cnn model'
    fi

    cd data/models/cnn
    if [ ! -f ResNet50.model ]; then
        wget https://www.dropbox.com/s/myf54v3845v09ff/ResNet50.model
    fi

    cd ../../

    if [ ! -d data/models/rnn ]; then
        mkdir --parents data/models/rnn
        echo 'Downloading pre-trained rnn model'
    fi
    
    cd data/models/rnn
    if [ ! -f STAIR_jp_256_Adam.model ]; then
        wget https://www.dropbox.com/s/8xmd8zhbzmdf5y9/STAIR_jp_256_Adam.model
    fi

    cd ../../

    if [ ! -d data/nic_dict ]; then
        mkdir --parents data/nic_dict
        echo 'Downloading Neural Image Caption Dictionary'
    fi

    cd data/nic_dict
    if [ ! -f dict_STAIR_jp_train.pkl ]; then
        wget https://www.dropbox.com/s/hqzgzh1txybfswd/dict_STAIR_jp_train.pkl
    fi

    cd ../../

    if [ ! -d data/word2vec ]; then
        mkdir --parents data/word2vec
        echo 'Downloading word2vec pre-trained model'
    fi

    cd data/word2vec
    if [ ! -f ja_wikipedia_neolog.model ]; then
        wget https://www.dropbox.com/s/9dxo5qhlezkc34a/ja_wikipedia_neolog.model
    fi
fi
