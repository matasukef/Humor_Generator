import os
from flask import session
from flask import Flask, render_template, request, url_for
import pandas as pd

from WEB_ENV import (
    EXP1_NUM,
    PRE_SURVEY_NUM,
    IMG_DIR_PATH,
    EXP1_DATA_PATH,
    PRE_SURVEY_PATH,
    EXP1_PATH,
)


def get_data_exp1(data_path, image_dir, num):
    csv_data = pd.read_csv(data_path)
    data = csv_data.sample(num)

    images = [os.path.join(image_dir, image.strip())
              .split('/', 1)[1] for image in data.iloc[:, 1]]
    cap_origin = [cap for cap in data.iloc[:, 2]]
    cap_ll = [cap for cap in data.iloc[:, 3]]
    cap_lh = [cap for cap in data.iloc[:, 4]]
    cap_hl = [cap for cap in data.iloc[:, 5]]
    cap_hh = [cap for cap in data.iloc[:, 6]]

    result = {'images': images, 'cap_origin': cap_origin,
              'cap_ll': cap_ll, 'cap_lh': cap_lh,
              'cap_hl': cap_hl, 'cap_hh': cap_hh
             }

    return result


def make_save_file():
    header = 'age,name,sex,'

    if not os.path.exists(PRE_SURVEY_PATH):
        pre_survey = header
        for i in range(1, PRE_SURVEY_NUM + 1):
            pre_survey += 'q' + str(i) + ','
        pre_survey =  pre_survey[:-1] + '\n'

        with open(PRE_SURVEY_PATH, 'w') as f:
            f.write(pre_survey)

    if not os.path.exists(EXP1_PATH):
        exp1 = header
        for i in range(1, EXP1_NUM + 1):
            exp1 += 'exp1_q' + str(i) + '_origin,'
            exp1 += 'exp1_q' + str(i) + '_ll,'
            exp1 += 'exp1_q' + str(i) + '_lh,'
            exp1 += 'exp1_q' + str(i) + '_hl,'
            exp1 += 'exp1_q' + str(i) + '_hh,'

        for i in range(1, EXP1_NUM + 1):
            exp1 += 'exp1_q' + str(i) + '_image,'

        exp1 =  exp1[:-1] + '\n'

        with open(EXP1_PATH, 'w') as f:
            f.write(exp1)


def save_data(question, session_data, save_path):

    if not _is_exist(session_data, save_path):
        body = ''

        for data in session_data.values():
            body += data + ','

        for value in question.values():
            body += value + ','

        body = body[:-1] + '\n'

        with open(save_path, 'a') as f:
            f.write(body)


def _is_valid(session):
    if session['name'] is None or session['age'] is None or session['sex'] is None:
        return False
    else:
        return True


def _is_exist(session, data_path):
    data = pd.read_csv(data_path)
    name = session['name']

    if name in data['name'].values:
        return True
    else:
        return False


def get_image_list(image_dir):
    file_list = [os.path.join(image_dir, img_path).split(
        '/', 1)[1] for img_path in os.listdir(image_dir)]

    return file_list


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET'])
def log_in():
    return render_template('index.html')


@app.route('/profile', methods=['GET'])
def experiment_description():

    return render_template('profile.html')


@app.route('/pre-survey', methods=['POST'])
def pre_survey():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['age'] = request.form['age']
        session['sex'] = request.form['sex']

    return render_template('pre_survey.html')


@app.route('/finish', methods=['POST'])
def finish_experiment():
    if request.method == 'POST':
        values = request.form
        save_data(values, session, EXP1_PATH)

    return render_template('finish.html')


@app.route('/experiment1', methods=['POST'])
def experiment1():
    if request.method == 'POST':
        if _is_valid(session):
            save_data(request.form, session, PRE_SURVEY_PATH)

    return render_template('experiment1_detail.html', experiment_no='システム評価実験', experiment_url='experiment1_content', exp_num=EXP1_NUM)


@app.route('/experiment1_content')
def experiment1_content():

    result = get_data_exp1(EXP1_DATA_PATH, IMG_DIR_PATH, EXP1_NUM)

    return render_template('experiment1.html', images=result['images'], cap_origin=result['cap_origin'], cap_ll=result['cap_ll'], cap_lh=result['cap_lh'], cap_hl=result['cap_hl'], cap_hh=result['cap_hh'])


if __name__ == '__main__':

    make_save_file()
    img_list = get_image_list(IMG_DIR_PATH)

    app.run(debug=True)
