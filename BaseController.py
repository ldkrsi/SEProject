from flask import Flask
from flask import render_template
from model import root as ModelRoot
from model import Account, User
app = Flask(__name__)

