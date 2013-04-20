from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
import Read_Data
@app.route('/_search')
def search():
    a = request.args.get('a', 0, type=str)
    #b = request.args.get('b', 0, type=int)
    res = Read_Data.work(a)
    return jsonify(result = res)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.debug = True
	Read_Data.preprocess()
	app.run()
