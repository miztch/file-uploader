import os
import secrets
from logging import getLogger

from flask import (Flask, flash, jsonify, make_response, redirect,
                   render_template, request, url_for)
from werkzeug.utils import secure_filename

import fileio
import util

logger = getLogger(__name__)

app = Flask(__name__, instance_relative_config=True)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

app.config.from_object('config')

bucket = os.envrion['S3_BUCKET']
table = os.environ['DYNAMODB_TABLE']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        files = fileio.list(table)
        no_records = False if files else True
        return render_template('index.html', files=files, no_records=no_records)
    else:
        # 入力項目の取得とチェック
        description = request.form.get('description')
        uploaded_file = request.files['file']

        valid, error_message = util.validate_input(description, uploaded_file)

        if valid:
            result = fileio.add(bucket, table, uploaded_file, description)

            flash('File uploaded', 'success')
            return redirect('/')

        # バリデーションエラーの場合にエラーを返す
        else:
            flash(error_message, 'danger')
            return redirect('/add')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/files/<string:file_id>')
def detail(file_id):
    file = fileio.get(bucket, table, file_id)

    return render_template('detail.html', file=file)


if __name__ == "__main__":
    app.run()
