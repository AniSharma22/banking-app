import uuid

from src.app.utils.types import Role
from typing import Dict



class User:

    def __init__(self, name: str, email: str, password: str, phone_no: str, address: str, id: str = None, role: str = Role.USER.value):
        # If no ID is provided, create a new UUID.
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.address = address
        self.role = role

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        # Validate input
        required_keys = ['name', 'email', 'password', 'phone_no', 'address']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required field: {key}")
        # Create user with default role as USER
        return cls(data['name'], data['email'], data['password'], data['phone_no'], data['address'])

