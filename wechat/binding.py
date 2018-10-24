from wechat import app
from flask import render_template, request
from controller.usercontrol import binding_control
from dao.userDao import UserDao


@app.route('/binding', methods=['GET', 'POST'])
def binding_page():
    if request.method == 'GET':
        if UserDao.select_user_flag(request.args.get("openid")) == 3:
            return render_template("error.html", error_info="")
        else:
            return render_template("binding.html", openid=request.args.get("openid"))
    if request.method == 'POST':
        user_info = {
            "openid": request.form.get('openid'),
            "username": request.form.get('name'),
            "password": request.form.get('pass')
        }
        binding_result = binding_control(user_info)
        if binding_result is True:
            return render_template("success.html")
        else:
            return render_template("error.html", error_info=binding_result)
