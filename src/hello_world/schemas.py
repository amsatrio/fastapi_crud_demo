from pydantic import BaseModel, Field

class HelloWorld(BaseModel):
    message: str = Field(
        default="hello", title="The description of the item", max_length=300, min_length=1, description="message must be valid string"
    )
