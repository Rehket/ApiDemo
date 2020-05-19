from sqlalchemy import Boolean, Column, Integer, String, DateTime, FetchedValue


from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    sys_revision = Column(Integer, server_default=FetchedValue())
    sys_created_date = Column(DateTime(timezone=True), server_default=FetchedValue())
    sys_modified_date = Column(DateTime(timezone=True), server_default=FetchedValue())
