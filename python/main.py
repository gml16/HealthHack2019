from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

def main():
    hello()

if __name__ == "__main__":
    main()
