import random
import string


def allowed_file(filename):
    allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_random_filename():
    length = 16
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def validate_input(description, file):
    '''
    validate input when a file addition requested
      - whether it has description text
      - whether the file is selected
      - whether the file extension is allowed
    '''

    result = False

    if not file.filename:
        msg = 'No files selcted.'
    elif file and allowed_file(file.filename) is False:
        msg = 'File extension is not allowed.'
    elif not description:
        msg = 'Enter description for upload file.'
    else:
        result = True

    if result:
        return result, ''
    else:
        return result, msg
