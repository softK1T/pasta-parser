# pasta_parser/main.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from mongo_utils import MongoDBClient

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
mongo_client = MongoDBClient()


@app.get("/pastas", response_model=List[dict])
async def get_pastas(
        limit: int = Query(10, gt=0, le=100, description="Number of items to return"),
        offset: int = Query(0, ge=0, description="The starting position of the query"),
        sort_by: str = Query("timestamp.$date", description="Field to sort by"),
        order: int = Query(-1, description="1 for ascending, -1 for descending"),
):
    try:
        # Check if sort_by field is valid
        valid_sort_fields = ["timestamp.$date", "overall_reactions", "author"]
        sort_field = sort_by if sort_by in valid_sort_fields else "timestamp.$date"

        # Fetch paginated results from MongoDB
        pastas = mongo_client.get_list(limit, offset, sort_field, order)

        return pastas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pasta/{pasta_id}", response_model=dict)
async def get_pasta(pasta_id: int):
    """
    Fetch a single pasta by its ID.
    :param pasta_id: ID of the pasta to fetch.
    """
    try:
        pasta = mongo_client.get_by_id(pasta_id)
        if not pasta:
            raise HTTPException(status_code=404, detail="Pasta not found")
        return pasta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# To run the server, use: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
