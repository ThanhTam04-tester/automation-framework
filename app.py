from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

users = [{"id": 1, "name": "Tam"}]


# ===== UI =====
@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "123":
            return redirect("/users")

    return render_template("login.html")


@app.route("/users")
def user_page():
    return render_template("users.html", users=users)


# ===== API =====
@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    new_user = {
        "id": len(users) + 1,
        "name": data.get("name")
    }

    users.append(new_user)

    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run(port=5000)