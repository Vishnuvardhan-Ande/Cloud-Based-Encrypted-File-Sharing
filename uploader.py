import uuid
import os
from config import supabase

def upload_file(filepath, owner):

    filename = os.path.basename(filepath)

    storage_name = f"{uuid.uuid4()}_{filename}"

    with open(filepath, "rb") as f:
        file_data = f.read()

    supabase.storage.from_("files").upload(
        path=storage_name,
        file=file_data,
        file_options={"content-type": "application/octet-stream"}
    )

    supabase.table("files").insert({
        "owner": owner,
        "filename": filename,
        "storage_path": storage_name
    }).execute()

    return storage_name