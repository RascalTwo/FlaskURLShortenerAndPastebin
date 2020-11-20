from flask import Flask, render_template, request, redirect

from typing import List, Optional



app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


shortened_urls: List[str] = []

@app.route('/shorten', methods=['POST'])
def shorten():
	url: str = request.form['url']
	if url not in shortened_urls:
		shortened_urls.append(url)
	index = shortened_urls.index(url)
	return render_template('shortened.html', shortened=index)

@app.route('/s/<shortened>')
def shortened_handler(shortened: int):
	try:
		shortened = int(shortened)
		if len(shortened_urls) > shortened:
			return redirect(shortened_urls[shortened])
	except:
		pass

	return render_template('404.html', message='Shortened URL not found'), 404


pastes: List[str] = []

@app.route('/paste', methods=['POST'])
@app.route('/paste/<id>', methods=['POST'])
def recieve_paste(id: Optional[int]=None):
	content: str = request.form['content']
	if content in pastes:
		id = pastes.index(content)

	if id:
		try:
			id = int(id)
		except:
			pass
		pastes[id] = content
	else:
		id = len(pastes)
		pastes.append(content)

	return render_template('paste.html', id=id, content=pastes[id])

@app.route('/p/<id>')
def paste(id: int):
	try:
		id = int(id)
		if len(pastes) > id:
			return render_template('paste.html', id=id, content=pastes[id])
	except:
		pass

	return render_template('404.html', message='Paste not found'), 404


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
