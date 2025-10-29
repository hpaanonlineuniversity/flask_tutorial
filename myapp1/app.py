from flask import Flask, request , make_response

app = Flask(__name__)



@app.route('/')
def index():
    return "<h2>Hi there</h2>\n"

@app.route('/hello', methods=['GET','POST'])
def hello():
    if request.method == 'GET':
        return "You made a Get request\n"
    elif request.method == 'POST':
        return "You made a POST request\n"
    else:
        return 'you will never see this message\n'
    
@app.route('/hi')
def hi():
    return "hi\n" , 201

@app.route('/hihi')
def hihi():
    response = make_response('hihi\n')
    response.status_code = 202
    response.headers['content-type'] = 'text/plain'
    return response


@app.route('/greet/<name>')
def greet(name):
    return f"<h2>Hello {name} !!!</h2>"

@app.route('/add/<int:num1>/<int:num2>')
def add(num1,num2):
    return f"{num1} + {num2} = {num1+num2}"

@app.route('/urlparas')
def urlparas():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
        return f'{greeting} {name}'
    else:
        return 'Some parameters are missing'


if __name__ == '__main__':
    app.run( host= '0.0.0.0', debug= True , port=5000)