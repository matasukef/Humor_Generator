import os
import argparse
from tqdm import tqdm
import pickle

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--formatted_json', '-j', type=str, default=os.path.join('..', 'static', 'captions', 'formatted_json_train_jp.pkl'), 
            help="input formatted json file which contains captions.")
    parser.add_argument('--img_dir', '-i', type=str, default=os.path.join(
        '..', 'static', 'images', 'mscoco_train'), help="input image dir")
    parser.add_argument('--output_csv_path', type=str, default=os.path.join('..', 'static', 'data', 'captions.csv'),
            help="output csv path")

    args = parser.parse_args()

    with open(args.output_csv_path, 'w') as f:
        header = 'no,caption,file_path\n'
        f.write(header)

    with open(args.formatted_json, 'rb') as f:
        data = pickle.load(f)

    images = os.listdir(args.img_dir)

    for i, img in tqdm(enumerate(images)):
        for caption in data:
            if img in caption['file_path']:
                cap = caption['captions'][0].strip('。')
                file_path = caption['file_path']
                break

        with open(args.output_csv_path, 'a') as f:
            cap_data = str(i) + ',' + cap + ',' + file_path + '\n'
            f.write(cap_data)
