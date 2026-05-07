from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

class Location(BaseModel):
    city: str = Field(..., description="City for the dining experience")
    neighborhood: Optional[str] = Field(None, description="Specific neighborhood")

class ReservationBookingRequest(BaseModel):
    restaurant_id: str = Field(..., description="ID of the restaurant on the platform")
    platform: str = Field(..., description="Platform to book on, e.g., 'resy' or 'tock'")
    party_size: int = Field(..., description="Number of guests", ge=1)
    reservation_date: datetime = Field(..., description="Date and time of the reservation")

    @field_validator('reservation_date')
    @classmethod
    def check_future_date(cls, v: datetime) -> datetime:
        if v.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
            raise ValueError('Reservation date must be in the future')
        return v

class EventTicketRequest(BaseModel):
    event_id: str = Field(..., description="ID of the ticketed event")
    platform: str = Field(default="tock", description="Platform, default 'tock'")
    party_size: int = Field(..., description="Number of tickets", ge=1)

class PaymentAuthorizationRequest(BaseModel):
    payment_token: str = Field(..., description="PCI-compliant payment token")
    amount: float = Field(..., description="Authorized amount", gt=0)
    currency: str = Field(default="USD", description="Currency code")
    platform: str = Field(default="rooam", description="Payment platform")

class DiningRecommendationRequest(BaseModel):
    cuisine_preferences: List[str] = Field(default_factory=list, description="Preferred cuisines")
    location: Location = Field(..., description="Location details")
    party_size: int = Field(..., description="Number of guests", ge=1)
    budget: Optional[str] = Field(None, description="Budget tier, e.g., '$$', '$$$'")
    target_date: Optional[datetime] = Field(None, description="Target date and time")

class UserPreferences(BaseModel):
    allergies: List[str] = Field(default_factory=list)
    dietary_restrictions: List[str] = Field(default_factory=list)
    favorite_cuisines: List[str] = Field(default_factory=list)
    disliked_ingredients: List[str] = Field(default_factory=list)
    average_spend: Optional[float] = None
    loyalty_status: Optional[str] = None
