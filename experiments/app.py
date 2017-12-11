import os
import sys
import argparse
import flask
from flask import session, redirect
from flask import Flask, render_template, request, jsonify, Response, url_for
from werkzeug import secure_filename
import random
import json
import csv
import pandas as pd

from WEB_ENV import (
        EXP1_NUM,
        EXP2_NUM,
        EXP3_NUM,
        PRE_SURVEY_NUM,
        IMG_DIR_PATH,
        EXP1_DATA_PATH,
        EXP2_DATA_PATH,
        EXP3_DATA_PATH,
        PRE_SURVEY_PATH,
        EXP1_PATH,
        EXP2_PATH,
        EXP3_PATH,
        RESULT_DIR,
    )



def get_data_exp1(data_path, image_dir, num):
    csv_data = pd.read_csv(data_path)
    data = csv_data.sample(num)
    
    images = [ os.path.join(image_dir, image.strip()).split('/', 1)[1] for image in data.iloc[:, 1]]
    captions = [ cap for cap in data.iloc[:, 2]]
    humor_captions = [ humor_cap for humor_cap in data.iloc[:, 3]]

    result = { 'images': images, 'captions': captions, 'humor_captions': humor_captions }

    return result

def get_data_exp2(data_path, image_dir, num):
    csv_data = pd.read_csv(data_path)
    data = csv_data.sample(num)

    images = [ os.path.join(image_dir, image.strip()).split('/', 1)[1] for image in data.iloc[:, 1]]
    humor_ll = [ humor_cap for humor_cap in data.iloc[:, 2]]
    humor_lm = [ humor_cap for humor_cap in data.iloc[:, 3]]
    humor_lh = [ humor_cap for humor_cap in data.iloc[:, 4]]
    humor_ml = [ humor_cap for humor_cap in data.iloc[:, 5]]
    humor_mm = [ humor_cap for humor_cap in data.iloc[:, 6]]
    humor_mh = [ humor_cap for humor_cap in data.iloc[:, 7]]
    humor_hl = [ humor_cap for humor_cap in data.iloc[:, 8]]
    humor_hm = [ humor_cap for humor_cap in data.iloc[:, 9]]
    humor_hh = [ humor_cap for humor_cap in data.iloc[:, 10]]

    result = {'images': images, 'cap_ll': humor_ll, 'cap_lm': humor_lm, 'cap_lh': humor_lh, 'cap_ml': humor_ml, 'cap_mm': humor_mm, 'cap_mh': humor_mh, 'cap_hl': humor_hl, 'cap_hm': humor_hm, 'cap_hh': humor_hh}

    return result


def get_data_exp3(data_path, image_dir, num):
    csv_data = pd.read_csv(data_path)
    data = csv_data.sample(num)
    
    images = [ os.path.join(image_dir, image.strip()).split('/', 1)[1] for image in data.iloc[:, 1]]
    captions = [ cap for cap in data.iloc[:, 2]]

    result = {'images': images, 'captions': captions}

    return result

def make_save_file():
    header = 'age,name,sex,student_id,'

    if not os.path.exists(PRE_SURVEY_PATH):
        pre_survey = header
        for i in range(1, PRE_SURVEY_NUM + 1):
            pre_survey += 'q' + str(i) + ','
        pre_survey += '\n'
        
        with open(PRE_SURVEY_PATH , 'w') as f:
            f.write(pre_survey)

    
    if not os.path.exists(EXP1_PATH):
        exp1 = header
        for i in range(1, EXP1_NUM + 1):
            exp1 += 'exp1_q' + str(i) + '_1,'
            exp1 += 'exp1_q' + str(i) + '_2,'

        for i in range(1, EXP1_NUM + 1):
            exp1 += 'exp1_q' + str(i) + '_image,'
        
        exp1 += '\n'
        
        with open(EXP1_PATH , 'w') as f:
            f.write(exp1)


    if not os.path.exists(EXP2_PATH):
        exp2 = header
        for i in range(1, EXP2_NUM + 1):
            exp2 += 'exp2_q' + str(i) + '_ll,'
            exp2 += 'exp2_q' + str(i) + '_lm,'
            exp2 += 'exp2_q' + str(i) + '_lh,'
            exp2 += 'exp2_q' + str(i) + '_ml,'
            exp2 += 'exp2_q' + str(i) + '_mm,'
            exp2 += 'exp2_q' + str(i) + '_mh,'
            exp2 += 'exp2_q' + str(i) + '_hl,'
            exp2 += 'exp2_q' + str(i) + '_hm,'
            exp2 += 'exp2_q' + str(i) + '_hh,'
        
        for i in range(1, EXP2_NUM + 1):
            exp2 += 'exp2_q' + str(i) + '_image,'
        
        exp2 += '\n'

        with open(EXP2_PATH , 'w') as f:
            f.write(exp2)
    
    if not os.path.exists(EXP3_PATH):
        exp3 = header
        for i in range(1, EXP3_NUM + 1):
            exp3 += 'exp3_q' + str(i) + ','

        for i in range(1, EXP3_NUM + 1):
            exp3 += 'exp3_q' + str(i) + '_image,'

        exp3 += '\n'
        
        with open(EXP3_PATH , 'w') as f:
            f.write(exp3)
        

def save_data(question, session_data, save_path):

    if not _is_exist(session_data, save_path):
        body = ''

        for data in session_data.values():
            body += data + ',' 

        for value in question.values():
            body += value + ','

        body += '\n'

        with open(save_path, 'a') as f:
            f.write(body)

def _is_valid(session):
    if session['name'] is None or session['age'] is None or session['sex'] is None or session['student_id'] is None:
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
    file_list = [ os.path.join(image_dir, img_path).split('/', 1)[1] for img_path in os.listdir(image_dir)]

    return file_list


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET'])
def log_in():
    return render_template('index.html')

@app.route('/description', methods=['POST'])
def experiment_description():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['age'] = request.form['age']
        session['sex'] = request.form['sex']
        session['student_id'] = request.form['student_id']

        if session['student_id'] is None:
            session['student_id'] = 'None'
        
    return render_template('description.html')

@app.route('/pre-survey')
def pre_survey():
    return render_template('pre_survey.html')

@app.route('/finish_experiment', methods=['POST'])
def finish_experiment():
    if request.method == 'POST':
        values = request.form
        referer =  request.headers.get('referer').split('/')[-1]
        
        if referer == 'experiment1_content':
            current_experiment_no = 'システム評価実験1'
            next_experiment_no = 'システム評価実験2'
            experiment_url = 'experiment2'
            save_data(values, session, EXP1_PATH)
        
        elif referer == 'experiment2_content':
            current_experiment_no = 'システム評価実験2'
            next_experiment_no = 'システム評価実験3'
            experiment_url = 'experiment3'
            save_data(values, session, EXP2_PATH)
    
    return render_template('finish_experiment.html', current_experiment_no = current_experiment_no, next_experiment_no = next_experiment_no, experiment_url = experiment_url)


@app.route('/finish', methods=['POST'])
def finish_all_experiment():
    if request.method == 'POST':
        values = request.form
        save_data(values, session, EXP3_PATH)
    
    return render_template('finish_all_experiment.html')


@app.route('/experiment1', methods=['POST'])
def experiment1():
    if request.method == 'POST':
        if _is_valid(session):
            save_data(request.form, session, PRE_SURVEY_PATH)
        
    return render_template('experiment1_detail.html', experiment_no = 'システム評価実験1', experiment_url = 'experiment1_content', exp_num = EXP1_NUM)


@app.route('/experiment1_content')
def experiment1_content():
    
    result = get_data_exp1(EXP1_DATA_PATH, IMG_DIR_PATH, EXP1_NUM)
    print(result['images'])

    return render_template('experiment1.html', images=result['images'], captions = result['captions'], humor_captions = result['humor_captions'])


@app.route('/experiment2', methods=['GET'])
def experiment2():
        
    return render_template('experiment2_detail.html', experiment_no = 'システム評価実験2', experiment_url = 'experiment2_content', exp_num=EXP2_NUM)    

@app.route('/experiment2_content')
def experiment2_content():

    result = get_data_exp2(EXP2_DATA_PATH, IMG_DIR_PATH, EXP2_NUM)

    return render_template('experiment2.html', images=result['images'], cap_ll = result['cap_ll'], cap_lm = result['cap_lm'], cap_lh = result['cap_lh'], cap_ml = result['cap_ml'], cap_mm = result['cap_mm'], cap_mh = result['cap_mh'], cap_hl = result['cap_hl'], cap_hm = result['cap_hm'], cap_hh = result['cap_hh'])

@app.route('/experiment3')
def experiment3():

    return render_template('experiment3_detail.html', experiment_no = 'システム評価実験3', experiment_url = 'experiment3_content', exp_num=EXP3_NUM)

@app.route('/experiment3_content')
def experiment3_content():

    result = get_data_exp3(EXP3_DATA_PATH, IMG_DIR_PATH, EXP3_NUM)

    return render_template('experiment3.html', images = result['images'], captions = result['captions'])


if __name__=='__main__':

    make_save_file()
    img_list = get_image_list(IMG_DIR_PATH)

    app.run(debug=True)
