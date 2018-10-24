from wechat import app
from flask import render_template, request
from dao.userDao import UserDao
from controller.scorecontrol import select_score
import json


@app.route('/score', methods=['GET'])
def show_score():
    if UserDao.select_user_flag(request.args.get("openid")) == 3:
        score = select_score(request.args.get("openid"))
        data_score = json.loads(score)
        return render_template("detail_score.html", data_score=data_score)
    else:
        return render_template("error.html", error_info="您未绑定")
