from cloudipsp import Api, Checkout
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./shop.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.name


@app.route("/")
def index():
    products = Product.query.order_by(Product.cost).all()
    return render_template("index.html", data=products)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method != "POST":
        return render_template("create.html")

    name = request.form["name"]
    cost = request.form["cost"]
    description = request.form["description"]

    product = Product(name=name, cost=cost, description=description)

    try:
        db.session.add(product)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "error"


@app.route("/buy/<int:id>")
def buy(id):
    product = Product.query.get(id)
    api = Api(merchant_id=1396424, secret_key="test")
    checkout = Checkout(api=api)
    data = {"currency": "USD", "amount": f"{str(product.cost)}00"}
    url = checkout.url(data).get("checkout_url")
    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True)
