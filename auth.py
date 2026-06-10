from werkzeug.security import generate_password_hash, check_password_hash
from config import supabase

def register_user(username, password):

    existing = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if existing.data:
        return False, "Username already exists"

    supabase.table("users").insert({
        "username": username,
        "password_hash": generate_password_hash(password)
    }).execute()

    return True, "Account created"


def verify_user(username, password):

    result = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if not result.data:
        return False

    return check_password_hash(
        result.data[0]["password_hash"],
        password
    )