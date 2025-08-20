import os
import pathlib
import tempfile

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Practice API", version="0.1.0")


class EchoRequest(BaseModel):
    message: str


class HelloRequest(BaseModel):
    text: str


class AddRequest(BaseModel):
    a: int
    b: int


class DropboxPdfRequest(BaseModel):
    folder_path: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to Practice API"}


@app.post("/echo")
def echo(payload: EchoRequest) -> dict[str, str]:
    return {"echo": payload.message}


@app.post("/hello")
def hello(payload: HelloRequest) -> dict[str, str]:
    return {"result": f"{payload.text} world"}


@app.post("/add")
def add(payload: AddRequest) -> dict[str, int]:
    return {"sum": payload.a + payload.b}


@app.post("/dropbox/pdfs")
def collect_dropbox_pdfs(payload: DropboxPdfRequest) -> dict[str, object]:
    """Download all PDFs under the given Dropbox folder and return filenames.

    Notes:
    - Requires env var `DROPBOX_ACCESS_TOKEN`.
    - Downloads into a temporary directory on the server.
    """
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if not access_token:
        raise HTTPException(
            status_code=500,
            detail="DROPBOX_ACCESS_TOKEN not configured",
        )

    try:
        import dropbox
        from dropbox.files import FileMetadata
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Dropbox SDK not available: {exc}")

    dbx = dropbox.Dropbox(access_token)

    # Normalize folder path: Dropbox expects "" for root, otherwise absolute like "/Folder/Sub"
    folder_input = (payload.folder_path or "").strip()
    if folder_input in ("", "/"):
        folder = ""
    else:
        folder = folder_input if folder_input.startswith("/") else f"/{folder_input}"

    pdf_entries: list[FileMetadata] = []
    try:
        result = dbx.files_list_folder(folder, recursive=True)
        while True:
            for entry in result.entries:
                if isinstance(entry, FileMetadata) and entry.name.lower().endswith(".pdf"):
                    pdf_entries.append(entry)
            if not result.has_more:
                break
            result = dbx.files_list_folder_continue(result.cursor)
    except dropbox.exceptions.ApiError as api_err:
        raise HTTPException(status_code=400, detail=f"Dropbox API error: {api_err}")
    except dropbox.exceptions.AuthError:
        raise HTTPException(status_code=401, detail="Invalid Dropbox access token")

    temp_dir = pathlib.Path(tempfile.mkdtemp(prefix="dropbox_pdfs_"))
    downloaded_filenames: list[str] = []

    for entry in pdf_entries:
        # Recreate the folder structure under the temp dir to avoid name clashes
        relative_path = entry.path_display.lstrip("/")
        local_path = temp_dir / relative_path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            dbx.files_download_to_file(str(local_path), entry.path_lower)
            downloaded_filenames.append(entry.name)
        except dropbox.exceptions.HttpError as http_err:
            # Skip files that fail to download and continue
            continue

    return {"files": downloaded_filenames, "count": len(downloaded_filenames)}

