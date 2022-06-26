import sys, json
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
# объявляем константы расширений и расположения контента
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORTFOLIO_DIR = 'portfolio'
# приложение
app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route('/')
def index():
    # добавление в список постов, если он лежит в папке, на которую ссылается POST_DIR
    posts = [post for post in flatpages if post.path.startswith(POST_DIR)] 
    posts.sort(key=lambda item: item['date'], reverse=True)
    cards = [card for card in flatpages if card.path.startswith(PORTFOLIO_DIR)]
    cards.sort(key=lambda item: item['title'])
    with open('settings.cfg', encoding='utf-8') as config:
        data = config.read()
        settings = json.loads(data)
    tags = set()
    for post in flatpages:
        tag = post.meta.get('tag')
        if tag:
            tags.add(tag.lower())
    return render_template('index.html', posts=posts, cards=cards, bigheader=True, tags=tags, **settings)


@app.route('/portfolio/<name>/')
def card(name):
    path = f'{PORTFOLIO_DIR}/{name}' # путь к карточке в портфолио
    card = flatpages.get_or_404(path)
    return render_template('card.html', card=card)


@app.route('/posts/<name>/')
def post(name):
    path = f'{POST_DIR}/{name}' # путь к посту в блоге
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)