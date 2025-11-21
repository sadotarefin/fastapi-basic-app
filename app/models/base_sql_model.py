from datetime import datetime, timezone
#from sqlalchemy import func, Column, DateTime          #too rigid with sql-alchemy
from sqlmodel import SQLModel, Field

#def strftime():
 #   return func.strftime('%Y-%m-%d %H:%M:%S', 'now')

def utc_now():
    return datetime.now(timezone.utc)

class BaseSqlModel(SQLModel):
    create_at: datetime = Field(
        default_factory=utc_now,
        nullable=False 
    )
    updated_at: datetime = Field(
        default_factory=utc_now, 
        nullable=False 
        #sa_column=Column(
         #   DateTime,
          #  nullable=False,
           # server_default=strftime()
        #)
    )
