import os
import re
from flask import (Blueprint, render_template, current_app,
                   request, url_for, redirect, abort)
from git import *
from gitdb import IStream
from StringIO import StringIO
import json


gitplugin = Blueprint('hgplugin', __name__, template_folder='templates')


"""
    Helpers
    ~~~~~~~
"""

"""
    Initializer
    ~~~~~~~~~~~
"""


def init(app):
    app.register_blueprint(gitplugin)
    app.signals.signal('page-saved').connect(git_commit)
    app.signals.signal('pre-display').connect(git_rev)
    app.signals.signal('pre-display').connect(extra_actions)
    app.git = GitManager(app.config['CONTENT_DIR'])
