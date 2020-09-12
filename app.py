from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://jmkim:jmkim@52.79.240.182', 27017)
db = client.buybutnotbuy


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/card-archive')
def archive():
    return render_template('index_List.html')


@app.route('/card', methods=['POST'])
def post_card():
    goal_receive = request.form['goal_give']
    name_receive = request.form['name_give']
    url_receive = request.form['url_give']
    story_receive = request.form['story_give']
    email_receive = request.form['email_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    patient_card = {'goal': goal_receive, 'name': name_receive, 'url': url_receive, 'story': story_receive,
                    'email': email_receive, 'image': url_image, 'title': url_title, 'desc': url_description,
                    'price': '', 'like': 0, 'bad': 0}

    db.patientcard.insert_one(patient_card)

    return jsonify({'result': 'success'})


@app.route('/card-list', methods=['GET'])
def read_card():
    card_list = list(db.patientcard.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'patient_card': card_list})


@app.route('/card-price', methods=['POST'])
def price_card():
    price_receive = request.form['price_give']
    url_receive = request.form['url_give']
    db.patientcard.update_one({'url': url_receive}, {'$set': {'price': price_receive}})
    return jsonify({'result': 'success', 'msg': 'like 연결되었습니다!'})


@app.route('/card/like', methods=['POST'])
def like_card():
    url_receive = request.form['url_give']
    url = db.patientcard.find_one({'url': url_receive})
    card_like = url['like'] + 1
    db.patientcard.update_one({'url': url_receive}, {'$set': {'like': card_like}})
    return jsonify({'result': 'success', 'msg': 'like 연결되었습니다!'})


@app.route('/card/bad', methods=['POST'])
def bad_card():
    url_receive = request.form['url_give']
    url = db.patientcard.find_one({'url': url_receive})
    card_bad = url['bad'] + 1
    db.patientcard.update_one({'url': url_receive}, {'$set': {'bad': card_bad}})
    return jsonify({'result': 'success', 'msg': 'like 연결되었습니다!'})


@app.route('/card/price/edit', methods=['POST'])
def edit_card():
    url_receive = request.form['url_give']
    price_receive = request.form['price_give']
    db.patientcard.update_one({'url': url_receive}, {'$set': {'price': price_receive}})
    return jsonify({'result': 'success', 'msg': 'like 연결되었습니다!'})


@app.route('/card/story/edit', methods=['POST'])
def edit_story_card():
    url_receive = request.form['url_give']
    story_receive = request.form['story_give']
    db.patientcard.update_one({'url': url_receive}, {'$set': {'story': story_receive}})
    return jsonify({'result': 'success', 'msg': 'like 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
