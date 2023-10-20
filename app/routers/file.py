import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings

# custom import
from app.models.file import InputModel
from app.services.file_service import parse_file

router = APIRouter()

embedding_model = GPT4AllEmbeddings()


def create_embeddings(text):
    query_result = embedding_model.embed_query(text)
    return query_result


@router.post("/v1/chunks")
def fetch_file(
    request_data: InputModel,
):
    file_url = request_data.url
    file_type = request_data.type
    chunk_data = request_data.chunks
    # Fetch the file
    print(file_type)
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

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_data.chunk_size,
            chunk_overlap=chunk_data.chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        documents = text_splitter.create_documents([parsed_text])
        output = {}
        chunks = [
            {
                "chunk": doc.page_content,
                "embeddings": create_embeddings(doc.page_content),
                "metadata": doc.metadata,
            }
            for doc in documents
        ]
        output["chunks"] = chunks
        return JSONResponse(content=output, status_code=200)
