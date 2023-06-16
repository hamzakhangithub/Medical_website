from flask import Flask, request, render_template
import requests

app = Flask(__name__)

base_url = "http://localhost:8000"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/medical_items")
def get_medical_items():
    response = requests.get(f"{base_url}/medical_items")
    medical_items = response.json()
    return render_template("medical_items.html", medical_items=medical_items)


@app.route("/medical_items/create", methods=["GET", "POST"])
def create_medical_item():
    if request.method == "POST":
        data = {
            "item_id": request.form["item_id"],
            "item_name": request.form["item_name"],
            "category": request.form["category"],
            "price": request.form["price"],
            "stock_quantity": request.form["stock_quantity"],
        }
        response = requests.post(f"{base_url}/medical_items", json=data)
        if response.status_code == 201:
            return render_template(
                "success.html", message="Medical item created successfully."
            )
        else:
            return render_template(
                "error.html", message="Failed to create medical item."
            )
    else:
        return render_template("create_medical_item.html")


@app.route("/medical_items/<int:id>")
def get_medical_item(id):
    response = requests.get(f"{base_url}/medical_items/{id}")
    medical_item = response.json()
    return render_template("medical_item.html", medical_item=medical_item)


@app.route("/medical_items/<int:id>/update", methods=["GET", "POST"])
def update_medical_item(id):
    response = requests.get(f"{base_url}/medical_items/{id}")
    medical_item = response.json()
    if request.method == "POST":
        data = {
            "item_name": request.form["item_name"],
            "category": request.form["category"],
            "price": request.form["price"],
            "stock_quantity": request.form["stock_quantity"],
        }
        response = requests.put(f"{base_url}/medical_items/{id}", json=data)
        if response.status_code == 200:
            return render_template(
                "success.html", message="Medical item updated successfully."
            )
        else:
            return render_template(
                "error.html", message="Failed to update medical item."
            )
    else:
        return render_template("update_medical_item.html", medical_item=medical_item)


@app.route("/medical_items/<int:id>/delete", methods=["GET", "POST"])
def delete_medical_item(id):
    response = requests.delete(f"{base_url}/medical_items/{id}")
    if response.status_code == 200:
        return render_template(
            "success.html", message="Medical item deleted successfully."
        )
    else:
        return render_template("error.html", message="Failed to delete medical item.")


if __name__ == "__main__":
    app.run(debug=True)
