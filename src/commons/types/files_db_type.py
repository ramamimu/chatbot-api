from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, timezone

class FilesEntity(BaseModel):
    id: int
    name: str
    filename: str
    created: str
    lastModified: str

    @model_validator(mode="before")
    def convert_datetimes_to_strings(cls, values):
        for dt_field in ['created', 'lastModified']:
            if isinstance(values.get(dt_field), datetime):
                dt = values.get(dt_field)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                values[dt_field] = dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
        return values

    class Config:
        orm_mode = True