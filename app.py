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

        # 説明が記載されていない場合にエラーを返す
        if description == '':
            flash('Enter description for upload file.', 'danger')
            return redirect('/add')

        # リクエストボディにファイルが存在しない場合にエラーを返す
        if 'file' not in request.files:
            flash('no file part', 'danger')
            return redirect('/add')

        # ファイル名が指定されていない場合にエラーを返す
        if uploaded_file.filename == '':
            flash('no files selected', 'danger')
            return redirect('/add')

        # 入力フォームのチェック後、ファイルそのものの処理
        if uploaded_file:
            # 許可された拡張子のファイルかチェックする
            # OKなら、S3へアップロードする際のファイル名を生成する
            if util.allowed_file(uploaded_file.filename):
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

            # 許可されていない拡張子の場合にエラーを返す
            else:
                flash('File extention is not allowed.', 'danger')
                return redirect('/add')


@app.route('/add')
def add():
    print(request.method)
    return render_template('add.html')

# --- below are paths for debug ---


@app.route('/scan')
def scan():
    return jsonify(dynamodb.scan(app.config['DYNAMODB_TABLE']))


@app.route('/get-all')
def get_all():
    return jsonify(dynamodb.get_all(app.config['DYNAMODB_TABLE']))


@app.route('/list-obj')
def list_obj():
    return jsonify(s3.list_object(app.config['S3_BUCKET']))


if __name__ == "__main__":
    app.run()
