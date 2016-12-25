from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from model import root as ModelRoot
from model import Account, User
app = Flask(__name__)

