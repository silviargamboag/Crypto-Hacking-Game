from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ =='__main__':
    app.run(debug = True)

from . import Usercontroller
app.register_blueprint(Usercontroller.bp)

from . import Authcontroller
app.register_blueprint(Authcontroller.bp)
