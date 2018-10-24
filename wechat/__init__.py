from flask import Flask

app = Flask(__name__)
app.debug = True

import wechat.binding
import wechat.index
import wechat.detailscore