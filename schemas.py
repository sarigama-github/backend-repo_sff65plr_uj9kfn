"""
Database Schemas for VisitPazar

Each Pydantic model represents a MongoDB collection. Collection name is the lowercase
of the class name (e.g., Place -> "place").
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class GeoLocation(BaseModel):
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    address: Optional[str] = Field(None, description="Street address or description")


class Place(BaseModel):
    """
    Places that appear on the map and in recommendations
    """
    name: str
    category: Literal[
        "restaurant", "cafe", "hotel", "museum", "landmark", "shop", "park", "other"
    ]
    description: Optional[str] = None
    location: GeoLocation
    images: List[str] = []
    contact_phone: Optional[str] = None
    contact_website: Optional[str] = None
    price_range: Optional[str] = Field(None, description="€, €€, €€€")
    rating: Optional[float] = Field(4.5, ge=0, le=5)
    is_featured: bool = Field(False, description="Sponsored or promoted partner")
    tags: List[str] = []


class Guide(BaseModel):
    name: str
    bio: Optional[str] = None
    languages: List[str] = ["sr", "en"]
    price_per_hour: float = 0.0
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    avatar_url: Optional[str] = None
    rating: Optional[float] = Field(4.6, ge=0, le=5)
    is_verified: bool = True


class Event(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    location: GeoLocation
    price: float = 0.0
    featured: bool = False
    image_url: Optional[str] = None
    categories: List[str] = []


class Booking(BaseModel):
    type: Literal["guide", "tour", "event", "restaurant"]
    reference_id: str = Field(..., description="ID of guide/place/event being booked")
    user_name: str
    user_contact: str
    date: datetime
    party_size: int = Field(1, ge=1)
    notes: Optional[str] = None

