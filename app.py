from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

# Routes


@app.route("/ping")
def ping():
    return jsonify({"message": "Pong!"})


@app.route("/products")
def get_products():
    return jsonify({"products": products, "message": "Products List"})


@app.route("/products/<string:product_name>")
def get_product(product_name):
    products_found = [
        product for product in products if product["name"] == product_name]

    if (len(products_found) > 0):
        return jsonify({
            "products_found": products_found[0]
        })

    return jsonify({"message": "Product with name '{}' wasn't found".format(product_name)})


@app.route("/products", methods=["POST"])
def add_product():
    new_product = {
        "name": request.json["name"],
        "price": request.json["price"],
        "quantity": request.json["quantity"]
    }

    products.append(new_product)

    return jsonify({
        "message": "Product added succesfully",
        "products": products
    })


@app.route("/products/<string:product_name>", methods=["PUT"])
def update_product(product_name):
    product_found = [
        product for product in products if product["name"] == product_name]
    if (len(product_found) > 0):
        product_found[0]["name"] = request.json["name"]
        product_found[0]["price"] = request.json["price"]
        product_found[0]["quantity"] = request.json["quantity"]

        return jsonify({
            "message": "Product '{}' was updated!".format(product_name),
            "product": product_found
        })
    return jsonify({
        "message": "Product with name '{}' wasn't found".format(product_name)
    })


@app.route("/products/<string:product_name>", methods=["DELETE"])
def delete_product(product_name):
    product_found = [
        product for product in products if product["name"] == product_name]
    if (len(product_found) > 0):
        products.remove(product_found[0])
        return jsonify({
            "message": "Product '{}' was deleted".format(product_name),
            "products": products
        })
    return jsonify({
        "message": "Product with name '{}' wasn't found".format(product_name)
    })


if __name__ == "__main__":
    app.run(debug=True, port=4000)
