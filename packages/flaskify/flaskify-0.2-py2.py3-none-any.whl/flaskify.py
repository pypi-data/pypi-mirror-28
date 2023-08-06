import click
import os
from json import load,dump

cfg = {
	"FLASK_APP" : "run.py",
	"VENV_PATH" : "venv/bin/",
	"ROUTES"    : "app/routes.py"
}

@click.group()
def cli():
	pass

@cli.command()
def run():
	if os.path.isfile(cfg['FLASK_APP']):
		os.system(
			'export FLASK_APP=%s\n%sflask run'
			% (cfg['FLASK_APP'], cfg['VENV_PATH']))
	else:
		click.echo('Cannot find \'%s\'' % cfg['FLASK_APP'])

@cli.command()
@click.option('--name', '-n',
	          prompt='project folder name',
			  help='Project folder name: No spaces')
def new(name):
	click.echo('Creating new project...')
	os.makedirs(name)
	os.system('python3 -m venv %s/venv' % name)
	os.system('%s/venv/bin/pip3 install wheel' % name)
	os.system('%s/venv/bin/pip3 install flask' % name)
	os.makedirs(name + '/app')
	os.makedirs(name + '/app/templates')
	os.makedirs(name + '/app/static')
	os.makedirs(name + '/app/static/css')
	os.makedirs(name + '/app/static/scss')
	routes = open(name + "/app/routes.py", "w+")
	config = open(name + "/config.py", "w+")
	run = open(name + "/run.py", "w+")
	init = open(name + "/app/__init__.py", "w+")
	base_html = open(name + "/app/templates/base.html", "w+")
	index_html = open(name + "/app/templates/index.html", "w+")
	base_css = open(name + "/app/static/css/base.css", "w+")
	index_css = open(name + "/app/static/css/index.css", "w+")


	init.write(
		"from flask import Flask\n\n"
		"app = Flask(__name__)\n"
		"app.config.from_object('config')\n"
		"from app import routes"
	)

	run.write(
		"#!venv/bin/python3\n\n"
		"from app import app\n"
		"app.run(debug=True)"
	)
	
	config.write(
		"SECRET_KEY = %s" % os.urandom(24)
	)

	routes.write(
		"from app import app\n"
		"from flask import render_template\n\n"
		"@app.route('/')\n"
		"@app.route('/index')\n"
		"def index():\n"
		"\treturn render_template('index.html')"
	)

	base_html.write(
		"<head>\n"
		"\t{% if title %}\n"
		"\t\t<title>{{ title }}</title>\n"
		"\t{% else %}\n"
		"\t\t<title>No title assigned</title>\n"
		"\t{% endif %}\n"
		'\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
		"\t<link href=\"{{ url_for(\'static\', filename=\'css/base.css\') }}\" rel=\"stylesheet\">\n"
		"\t{% block head %}{% endblock %}\n"
		"</head>\n\n"
		"<body>\n"
		"\t<div class=\"nav\">\n"
		"\t\t<a class=\"nav-item\" href=\"\">\n"
		"\t\t\t<p></p>\n"
		"\t\t</a>\n"
		"\t</div>\n"
		"\t{% block body %}{% endblock %}"
		"</body>"
	)

	index_html.write("{% extends 'base.html' %}")
	base_css.write(
		".nav {\n"
		"\tdisplay: grid;\n"
		"\tgrid-template-columns: repeat(4, 1fr);\n"
		"\theight: auto;\n"
		"\tposition: sticky;\n"
		"\ttop: 0;\n"
		"\tbackground-color: rgba(255,255,255,.3);\n"
		"}\n\n"
		".nav-item {\n"
		"\ttext-align: center;\n"
		"\ttext-decoration: none;\n"
		"\tcolor: inherit;\n"
		"}\n\n"
		".nav-item:hover {\n"
		"\tcolor: rgba(0,0,0,.3);\n"
		"}\n\n"
		".nav-item:focus {\n"
		"\toutline: none;\n"
		"}"
	)

	routes.close()
	config.close()
	run.close()
	init.close()
	base_html.close()
	index_html.close()
	base_css.close()
	index_css.close()