from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

class FoodBase(BaseModel):
    """
    Base model for common food attributes.
    This helps in avoiding repetition.
    """
    name: str = Field(..., min_length=2, max_length=100,
                       description="Name of the food item.")
    calories: int = Field(..., gt=0, description="Caloric content per serving.")
    description: str = Field(..., max_length=500,
                            description="A brief description of the food item.")

class FoodCreate(FoodBase):
    """
    Model for creating a new food item.
    Inherits all fields from FoodBase.
    """
    pass

class Food(FoodBase):
    """
    Model representing a food item as stored in the database,
    including its unique identifier.
    """
    model_config = ConfigDict(populate_by_name=True) # Allows initialization with `_id` or `id`

    id: UUID = Field(default_factory=uuid4, alias="_id",
                     description="Unique identifier for the food item.")

class FoodUpdate(BaseModel):
    """
    Model for updating an existing food item.
    All mutable fields are optional, allowing partial updates.
    Filed id is required to identify the food item to update.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(default_factory=uuid4, alias="_id",
                     description="Unique identifier for the food item.")

    name: Optional[str] = Field(None, min_length=2, max_length=100,
                                description="Updated name of the food item.")
    calories: Optional[int] = Field(None, gt=0,
                                   description="Updated caloric content per serving.")
    description: Optional[str] = Field(None, max_length=500,
                                    description="Updated description of the food item.")