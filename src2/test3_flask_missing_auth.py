# test3_flask_missing_auth.py
from flask import Flask, request
app = Flask(__name__)

# ❌ Missing authentication on sensitive route
@app.route("/user/profile")
def profile():
    # No session check, token check, or identity gateway
    return {"profile": "private user data"}

# ❌ Trusts user-supplied query parameter for identity
@app.route("/admin")
def admin_area():
    user = request.args.get("user")
    role = request.args.get("role")

    if role == "admin":
        return "Admin Access Granted"

    return "Access Denied"

app.run()
