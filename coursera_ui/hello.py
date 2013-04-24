from flask import Flask, jsonify, render_template, request, redirect
app = Flask(__name__)
import Read_Data
import mit_parse
import spell_check
import isbn

@app.route('/_search')
def search():
    a = request.args.get('a', 0, type=str)
    #b = request.args.get('b', 0, type=int)
    b = [spell_check.correct(x) for x in a.split()]
    actual_q = ''
    for word in a.split():
    	actual_q = actual_q + word + ' '
    	
    query = ''
    for word in b:
    	query = query + word + ' '

    res = Read_Data.work(query)
    return jsonify(result = res)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/_search_isbn')
def search_mit():
	a = request.args.get('a', 0, type=str)
	b = [spell_check.correct(x) for x in a.split()]
	actual_q = ''
	for word in a.split():
		actual_q = actual_q + word + ' '
	
	query = ''
	for word in b:
		query = query + word + ' '
	res = isbn.getisbnData(query)
	return jsonify(result = res)
    
if __name__ == '__main__':
	app.debug = True
	Read_Data.preprocess()
	#mit_parse.preprocess()
	app.run()
