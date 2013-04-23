from flask import Flask, jsonify, render_template, request, redirect
app = Flask(__name__)
import Read_Data
import mit_parse

@app.route('/_search')
def search():
    a = request.args.get('a', 0, type=str)
    #b = request.args.get('b', 0, type=int)
    res = Read_Data.work(a)
    return jsonify(result = res)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/_search_mit')
def search_mit():
	a = request.args.get('a', 0, type=str)
	res = mit_parse.work(a)
	return jsonify(result = res)
    
if __name__ == '__main__':
	app.debug = True
	Read_Data.preprocess()
	mit_parse.preprocess()
	app.run()
