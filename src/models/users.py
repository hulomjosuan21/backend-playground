import uuid
from src.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class AuthMethodEnum(enum.Enum):
    EMAIL = "email"
    GOOGLE = "google"

class UserRoleEnum(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)

    auth_method = db.Column(db.Enum(AuthMethodEnum, name='auth_method_enum'), nullable=False)
    role = db.Column(db.Enum(UserRoleEnum, name='user_role_enum'), nullable=False, default=UserRoleEnum.CUSTOMER)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_password_hash(plaintext_password)

    def check_password(self, plaintext_password):
        return check_password_hash(self._password, plaintext_password)
    
    def to_dict(self, include_password=False):
        result = {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'auth_method': self.auth_method.value,
            'role': self.role.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if include_password:
            result['password'] = self._password

        return result