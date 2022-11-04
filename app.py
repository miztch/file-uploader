import io
import datetime
import secrets
import string
import random

from flask import Flask, flash, render_template, request, redirect, url_for, make_response, jsonify
from logging import getLogger
from werkzeug.utils import secure_filename

import dynamodb
import s3
import util

logger = getLogger(__name__)

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

app.config.from_pyfile('./config.cfg')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        files = dynamodb.get_all(app.config['DYNAMODB_TABLE'])
        no_records = False if files else True
        return render_template('index.html', files=files, no_records=no_records)
    else:
        # 入力項目の取得とチェック
        description = request.form.get('description')
        uploaded_file = request.files['file']

        valid, error_message = util.validate_input(description, uploaded_file)

        if valid:
            # S3へアップロードする際のファイル名を生成する
            extension = uploaded_file.filename.rsplit('.', 1)[1].lower()
            file_id = util.generate_random_filename()
            s3_key = file_id + '.' + extension
            upload_data = io.BufferedReader(uploaded_file).read()

            # S3へアップロードする
            result = s3.put_object(
                app.config['S3_BUCKET'],
                upload_data,
                s3_key
            )

            # DynamoDBへレコードを追加する
            item = {
                'file_id': file_id,
                'description': description,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                's3_key': s3_key
            }

            dynamodb.put(app.config['DYNAMODB_TABLE'], item)

            flash('File uploaded', 'success')
            return redirect('/')

        # バリデーションエラーの場合にエラーを返す
        else:
            flash(error_message, 'danger')
            return redirect('/add')


@app.route('/add')
def add():
    print(request.method)
    return render_template('add.html')


@app.route('/files/<string:file_id>')
def detail(file_id):
    record = dynamodb.get(app.config['DYNAMODB_TABLE'], file_id)

    s3_key = record['Item']['s3_key']
    timestamp = record['Item']['timestamp']

    s3_object = s3.get_object(
        app.config['S3_BUCKET'], s3_key)

    presigned_url = s3.generate_presigned_url(
        app.config['S3_BUCKET'], s3_key)

    file = {
        'file_id': file_id,
        's3_key': s3_key,
        'timestamp': timestamp,
        'presigned_url': presigned_url
    }

    return render_template('detail.html', file=file)


if __name__ == "__main__":
    app.run()
