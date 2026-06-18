from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
import os

# Resolve absolute paths for static roots so the server works no matter the CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'app', 'static')
ASSETS_ROOT = os.path.join(STATIC_ROOT, 'assets')
CSS_ROOT = os.path.join(STATIC_ROOT, 'css')
JS_ROOT = os.path.join(STATIC_ROOT, 'js')
IMG_ROOT = os.path.join(STATIC_ROOT, 'img')

app = Bottle()
ctl = Application()

#-----------------------------------------------------------------------------
# Rotas Estáticas e Helper:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=STATIC_ROOT)

@app.route('/css/<filepath:path>')
def serve_css(filepath):
    return static_file(filepath, root=CSS_ROOT)

@app.route('/js/<filepath:path>')
def serve_js(filepath):
    return static_file(filepath, root=JS_ROOT)

@app.route('/images/<filepath:path>')
def serve_images(filepath):
    return static_file(filepath, root=IMG_ROOT)

@app.route('/assets/<filepath:path>')
def serve_assets(filepath):
    return static_file(filepath, root=ASSETS_ROOT)

@app.route('/')
@app.route('/index')
def index():
    return ctl.render('index')

@app.route('/helper')
def helper():
    return ctl.render('helper')

#-----------------------------------------------------------------------------
# Rotas Principais:

@app.route('/pagina')
@app.route('/pagina/<parametro>') 
def action_pagina(parametro=None):
    # Alterei o nome da variável de "username" para "parametro" 
    # para fazer sentido quando você digitar "/pagina/0"
    if not parametro:
        return ctl.render('pagina')
    else:
        return ctl.render('pagina', parametro)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Lembre-se: se "username" aqui for uma palavra (ex: "admin"),
    # o redirect abaixo vai falhar no "int(parameter)" do seu DataRecord.
    session_id, username = ctl.authenticate_user(username, password)
    
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        redirect(f'/pagina/{username}')
    else:
        redirect('/portal')
    
@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/helper')

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
