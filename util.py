import random
import string


def allowed_file(filename):
    allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_random_filename():
    length = 16
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
