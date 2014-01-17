#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""This plugin versions your content into mercurial repository

Optional config:

    ``HG_REMOTE`` remote repository for pushin and pulling changes

"""

#===============================================================================
# IMPORTS
#===============================================================================

import os
import datetime

from flask import (Blueprint, render_template, current_app,
                   request, url_for, redirect, abort)
from flask.ext.script import Command

import hgapi


#===============================================================================
# CONSTANTS
#===============================================================================

PLUGIN_NAME = "waliki-hgplugin"


#===============================================================================
# BLUEPRINT
#===============================================================================

hgplugin = Blueprint(PLUGIN_NAME, __name__, template_folder='templates')


#===============================================================================
# SLOTS
#===============================================================================

def _msg(**kwargs):
    dt = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    msg = kwargs.get("message", "Autocommit of hg-waliki-plugin")
    return "[{}] {}".format(dt, msg)


def hg_commit(page, **kwargs):
    msg = _msg(**kwargs)
    user = kwargs["user"].name if "user" in kwargs else "NN"
    try:
        current_app.hg.hg_addremove()
        current_app.hg.hg_commit(msg, user)
    except hgapi.HgException as err:
        pass

#===============================================================================
#
#===============================================================================

class CmdHgCiPush(Command):
    """Push the content to HG server located in 'HG_REMOTE' config"""

    def run(self):
        current_app.hg.hg_addremove()
        current_app.hg.hg_commit(_msg(), "NN")
        remote = current_app.config['HG_REMOTE']
        current_app.hg.hg_push(remote)


class CmdHgPullUpdate(Command):
    """Retrieve all the content located at 'HG_REMOTE' config"""

    def run(self):
        remote = current_app.config['HG_REMOTE']
        current_app.hg.hg_pull(remote)
        current_app.hg.hg_update("tip")


#===============================================================================
# INITS
#===============================================================================

def init(app):
    # register plugin
    app.register_blueprint(hgplugin)

    # register signals
    app.signals.signal('page-saved').connect(hg_commit)

    # add cli commands
    app.manager.add_command("content-hg-ci-push", CmdHgPush())
    app.manager.add_command("content-hg-pull-u", CmdHgPullUpdate())

    # init repository
    app.hg = hgapi.Repo(app.config['CONTENT_DIR'])
    try:
        app.hg.hg_init()
    except hgapi.HgException as err:
        pass
    else:
        msg = "-".join([
            HG_COMMIT_MSG.substitute(datetime=datetime.datetime.utcnow()),
            "first commit"
        ])
        user = PLUGIN_NAME
        app.hg.hg_addremove()
        app.hg.hg_commit(msg, user)
    if 'HG_REMOTE' in app.config:
        app.hg.hg_pull(app.config.get('HG_REMOTE'))
    app.hg.hg_update("tip")




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
