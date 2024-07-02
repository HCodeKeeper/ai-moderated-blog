from typing import Optional

from ninja import Schema


class UserOutSchema(Schema):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
