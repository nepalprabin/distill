import requests
from fastapi import APIRouter, HTTPException

# custom import
from app.models.file_model import InputModel
from app.services.file_service import parse_file

router = APIRouter()


@router.post("/v1/parse-data")
def fetch_file(
    request_data: InputModel,
):
    file_url = request_data.url
    file_type = request_data.type
    text = request_data.text
    # Fetch the file

    if file_type in ["pdf", "txt", "docx"]:
        print("Here")
        response = requests.get(file_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Unsupported file type. Supported file types are PDF, DOCX, and TXT",
            )

        # Get file type from the URL
        # Extracting Content-Type header
        content_type = response.headers.get("Content-Type")
        print("Content_Type", content_type)
        MIME_MAP = {
            "application/pdf": "pdf",
            "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "text/plain": "txt",
        }

        url_file_type = MIME_MAP.get(content_type, "unknown")
        parsed_text = parse_file(url_file_type, response)
        return parsed_text
