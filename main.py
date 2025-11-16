import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import Place, Guide, Event, Booking

app = FastAPI(title="VisitPazar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "VisitPazar Backend is running"}


# Simple public lists for prototype
@app.get("/api/places")
def list_places(category: Optional[str] = None, featured: Optional[bool] = None):
    filt = {}
    if category:
        filt["category"] = category
    if featured is not None:
        filt["is_featured"] = featured
    places = get_documents("place", filt, limit=100)

    # Convert ObjectId to string
    for p in places:
        p["_id"] = str(p.get("_id"))
    return {"items": places}


@app.post("/api/places")
def create_place(place: Place):
    try:
        inserted_id = create_document("place", place)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/guides")
def list_guides():
    guides = get_documents("guide", {}, limit=100)
    for g in guides:
        g["_id"] = str(g.get("_id"))
    return {"items": guides}


@app.post("/api/guides")
def create_guide(guide: Guide):
    try:
        inserted_id = create_document("guide", guide)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events")
def list_events():
    events = get_documents("event", {}, limit=100)
    for ev in events:
        ev["_id"] = str(ev.get("_id"))
    return {"items": events}


@app.post("/api/events")
def create_event(event: Event):
    try:
        inserted_id = create_document("event", event)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/bookings")
def create_booking(booking: Booking):
    try:
        inserted_id = create_document("booking", booking)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
