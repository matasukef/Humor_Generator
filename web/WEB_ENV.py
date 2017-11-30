import os
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploader')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#parameters
NUM_IMG_OUTPUT = 10
NUM_IMG_CUTOFF = 1
IMG_SIM = 'high'
WORD_SIM = 'low'
