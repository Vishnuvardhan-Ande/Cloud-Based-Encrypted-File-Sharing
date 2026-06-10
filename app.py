import os
import secrets
from flask import send_file
from io import BytesIO
from datetime import datetime, timedelta

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from auth import register_user, verify_user
from uploader import upload_file
from config import supabase

from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-secret"
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def login_required(f):

    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):

        if "username" not in session:
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return wrapper


@app.route("/")
def home():

    if "username" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        ok, msg = register_user(
            username,
            password
        )

        flash(msg)

        if ok:
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):

            session["username"] = username

            return redirect(
                url_for("dashboard")
            )

        flash("Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

@app.route("/share/<file_id>", methods=["GET", "POST"])
@login_required
def share(file_id):

    if request.method == "POST":

        password = request.form["password"]

        token = secrets.token_urlsafe(32)

        expiry = datetime.utcnow() + timedelta(days=1)

        print("FILE ID RECEIVED:", file_id)

        supabase.table("files").update({
            "share_token": token,
            "share_password_hash": generate_password_hash(password),
            "share_expiry": expiry.isoformat()
        }).eq("id", file_id).execute()

        result = supabase.table("files").update({
            "share_token": token,
            "share_password_hash": generate_password_hash(password),
            "share_expiry": expiry.isoformat()
        }).eq("id", file_id).execute()

        print(result)

        share_link = request.host_url + "shared/" + token

    return render_template(
        "share_success.html",
        share_link=share_link
    )

@app.route("/shared/<token>", methods=["GET", "POST"])
def shared(token):

    result = supabase.table("files")\
        .select("*")\
        .eq("share_token", token)\
        .execute()

    if not result.data:
        return "Invalid Share Link"

    file = result.data[0]

    if request.method == "POST":

        password = request.form["password"]

        if check_password_hash(
            file["share_password_hash"],
            password
        ):

            file_data = supabase.storage \
                .from_("files") \
                .download(file["storage_path"])

            filename = file["filename"]

            return send_file(
                BytesIO(file_data),
                as_attachment=True,
                download_name=filename
            )

        flash("Wrong Password")

    return render_template(
        "shared_access.html"
    )

@app.route("/dashboard")
@login_required
def dashboard():

    username = session["username"]

    files = supabase.table("files") \
        .select("*") \
        .eq("owner", username) \
        .execute() \
        .data

    return render_template(
        "dashboard.html",
        username=username,
        files=files
    )


@app.route("/upload", methods=["POST"])
@login_required
def upload():

    file = request.files["file"]

    filename = secure_filename(
        file.filename
    )

    temp_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(temp_path)

    upload_file(
        temp_path,
        session["username"]
    )

    os.remove(temp_path)

    flash("File uploaded successfully")

    return redirect(
        url_for("dashboard")
    )


@app.route("/download/<path:storage_path>")
@login_required
def download(storage_path):

    file_data = supabase.storage \
        .from_("files") \
        .download(storage_path)

    original_filename = storage_path.split("_", 1)[1]

    return send_file(
        BytesIO(file_data),
        as_attachment=True,
        download_name=original_filename
    )

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)