from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
import sqlite3
import math
import json
import datetime
from urllib.parse import unquote

app = Flask(__name__)

results_per_page = 30
dbname = 'movies.db'
cols = "descr_id as id, filmweb_url, synopsis"

@app.route('/')
def index():
	return redirect(url_for(f'movies'))

@app.route('/movies')
def movies():
	page = request.args.get('page', default=1, type=int)
	offset = (page-1) * results_per_page
	with sqlite3.connect(dbname) as conn:
		conn.row_factory = sqlite3.Row
		rows = conn.execute(f'select {cols} from movies order by descr_id limit {results_per_page} offset {offset}').fetchall()
		
		rows_as_dicts = [dict(row) for row in rows]
		
		for row in rows_as_dicts:
			if row["filmweb_url"]:
				url = unquote(row["filmweb_url"]).replace('+', ' ')
				segment = url.split('/')[4]
				parts = segment.split('-')
				row['title'] = parts[0]
				row['year'] = parts[1]

		total_results = conn.execute(f'select count(*) from movies').fetchone()[0]
		##page_count = math.ceil(count/page_size)
		total_pages = math.ceil(total_results/results_per_page)
		##page_range = range(1, page_count+1)

		# Oblicz zakres paginacji
		start_page = max(1, page - 3)
		end_page = min(total_pages, page + 3)

	return render_template('movies.html', movies=rows_as_dicts, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)

@app.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
	if request.method == 'GET':
		with sqlite3.connect(dbname) as conn:
			conn.row_factory = sqlite3.Row
			row = conn.execute(f'select {cols} from movies where descr_id = {id}').fetchone()
			return render_template('details.html', movie=row)
	if request.method == 'POST':
		return redirect(url_for(f'details', id=id))

@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'GET':
		return render_template('create.html')
	if request.method == 'POST':
		with sqlite3.connect(dbname) as conn:
			title = request.form.get('title')
			descr = request.form.get('descr')
			cursor = conn.cursor()
			cursor.execute(f'insert into movies({cols}) values(NULL,?,?,?,?)', (title,descr,datetime.datetime.now(),datetime.datetime.now()))
			return redirect(url_for(f'details', id=cursor.lastrowid))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	if request.method == 'GET':
		with sqlite3.connect(dbname) as conn:
			conn.row_factory = sqlite3.Row
			row = conn.execute(f'select {cols} from movies where descr_id = {id}').fetchone()
			return render_template('update.html', movie=row)
	if request.method == 'POST':
		with sqlite3.connect(dbname) as conn:
			synopsis = request.form.get('synopsis')
			filmweb_url = request.form.get('filmweb_url')
			cursor = conn.cursor()
			cursor.execute(f'update movies set synopsis=?,filmweb_url=? where descr_id=?', (synopsis,filmweb_url,id))
			return redirect(url_for(f'details', id=id))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

# Custom filter to format date
@app.template_filter('format_datetime')
def format_datetime(value):
	return value[:10]

if __name__=="__main__":
	app.run(host='0.0.0.0', port=8080)
