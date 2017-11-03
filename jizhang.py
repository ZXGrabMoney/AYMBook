#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 
# created by yjweng01 on 02-11-17
# debug by yjweng01 and minghust on 03-11-17
#

from flask import Flask, request
import smtplib
import sqlite3
from email.mime.text import MIMEText
import random

userList = []
app = Flask(__name__)


def createVerifiedCode():
    chars = ['0','1','2','3','4','5','6','7','8','9']
    x = random.choice(chars),random.choice(chars),random.choice(chars),random.choice(chars)
    verifycode = "".join(x)
    return verifycode


def sendmail(email, code):
	_user = "2856817781@qq.com"
	_pwd = "ksiuoasxojpfdceb"
	_to = email
 
	msg = MIMEText("欢迎注册轻记账！您的校验码是：%s"%code)
	msg["Subject"] = "轻记账校验码"
	msg["From"] = _user
	msg["To"] = _to

	try:
		s = smtplib.SMTP_SSL("smtp.qq.com", 465)
		s.login(_user, _pwd)
		s.sendmail(_user, _to, msg.as_string())
		s.quit()
		print ("Success!")
	except smtplib.SMTPException:
		print ("Falied,%s")

@app.route('/getcode/',methods = ['GET','POST'])
def getcode():
	if request.method == 'POST': 
		db = sqlite3.connect('database.db')
		cur = db.cursor()
		dic = { "userEmail":"", "password": "", "code":""}

		em_list = list()
		em_list.append(request.form['email'])
		a = tuple(em_list)
		whether_exit = cur.execute("select * from user where email = ?",a).fetchall()
		db.close()
		if whether_exit:
			return "False" # If the mail has been registed, return "False" to show that.
		else:
			print("here")
			code = createVerifiedCode()
			sendmail(request.form['email'], code)
			dic["userEmail"] = request.form['email']
			dic["password"] = request.form['password']
			dic["code"] = code
			userList.append(dic)
			return "True"


@app.route('/register/',methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		db = sqlite3.connect('database.db')
		cur = db.cursor()
		for em in userList:
			if em["userEmail"] == request.form['email']:
				if request.form['code'] == em["code"]:
					em_list = list()
					em_list.append(request.form['email'])
					em_list.append(request.form['password'])
					a = tuple(em_list)
					cur.execute("INSERT INTO user VALUES (?,?)",a)
					cur.close()
					db.commit()
					db.close()
					userList.remove(em)
					return "success" # 注册成功 跳转页面
				else:
					return "codeError" # 验证码错误
		return "emailError" # 找不到该邮箱

@app.route('/login/',methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		db = sqlite3.connect('database.db')
		cur = db.cursor()
		em_list = list()
		em_list.append(request.form['email'])
		a = tuple(em_list)
		cur.execute("select * from user where email = ?",a)
		whether_exist = cur.fetchall()
		cur.close()
		db.close()
		if whether_exist == []:
			return "emailError" #用户不存在
		elif request.form['password'] != whether_exist[0][1]:
			return "passwordError" # 密码输入错误
		else:
			return "success" # 密码输入正确，成功登陆

if __name__ == '__main__':
	app.run(
        host = '0.0.0.0',
        port = 5050,
    )