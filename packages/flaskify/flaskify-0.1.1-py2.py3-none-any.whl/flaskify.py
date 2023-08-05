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

@cli.group()
def generate():
	pass

@generate.command()
@click.option('--name', '-n',
	          prompt='project folder name',
			  help='Project folder name: No spaces')
def project(name):
	click.echo('Generating project...')
	os.makedirs(name)
	os.system('python3 -m venv %s/venv' % name)
	os.system('%s/venv/bin/pip3 install wheel' % name)
	os.system('%s/venv/bin/pip3 install flask' % name)
	os.makedirs(name + '/app')
	os.makedirs(name + '/app/templates')
	os.makedirs(name + '/app/static')
	os.makedirs(name + '/app/static/css')
	routes = open(name + "/app/routes.py", "w+")
	config = open(name + "/config.py", "w+")
	run = open(name + "/run.py", "w+")
	init = open(name + "/app/__init__.py", "w+")
	index_html = open(name + "/app/templates/index.html", "w+")
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

	index_html.write(
		"<head>\n"
		"\t<title>Placeholder title</title>\n"
		'\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
		"\t<link href=\"{{ url_for(\'static\', filename=\'css/index.css\') }}\" rel=\"stylesheet\">\n"
		"</head>"
	)

	routes.close()
	config.close()
	run.close()
	init.close()
	index_html.close()
	index_css.close()

@generate.command()
@click.option('--name', prompt='route name')
@click.option('--template_name', prompt='html template name')
def route(name, template_name):
	string = "\n\n@app.route('/%s')\n" % name
	string += "def %s():\n\treturn render_template('%s.html')\n" % (name,name)
	if os.path.isfile(cfg['ROUTES']):
		f = open(cfg['ROUTES'], 'a+')
		html = open('app/templates/' + template_name + '.html', "w+")
		css = open('app/static/css/' + template_name + '.css', "w+")
		
		f.write(string)
		html.write(
			"<head>\n"
			"\t<title>Placeholder title</title>\n"
			'\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
			"\t<link href=\"{{ url_for(\'static\', filename=\'css/" + template_name + ".css\') }}\" rel=\"stylesheet\">\n"
			"</head>"
		)

		f.close()
		html.close()
		css.close()
	else:
		click.echo('cannot find \'app/routes.py\'')