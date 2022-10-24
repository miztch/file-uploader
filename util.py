import random
import string

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_random_filename():
    length = 16
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
