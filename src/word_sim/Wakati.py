import sys
import argparse
import MeCab

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', '-i', type=str, defalut=os.path.join)
