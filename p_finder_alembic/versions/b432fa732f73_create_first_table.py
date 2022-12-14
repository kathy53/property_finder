"""create first table

Revision ID: b432fa732f73
Revises: 
Create Date: 2022-11-21 17:35:41.912751

house_id should be the primary key
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b432fa732f73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """CREATE TABLE houses(
            house_id INTEGER NOT NULL AUTO_INCREMENT,
            title TEXT,
            location VARCHAR(255),
            description TEXT,
            price INTEGER,
            category VARCHAR(100),
            subcategory VARCHAR(100),
            bedrooms INTEGER,
            total_rooms INTEGER,
            car_spaces INTEGER,
            bathrooms INTEGER,
            building_size INTEGER,
            land_size INTEGER,
            furnished BOOLEAN,
            year_built INTEGER,
            geo_point TEXT,
            image_url TEXT,
            PRIMARY KEY (house_id) 
        )"""
    )


def downgrade() -> None:
    op.execute(
        """DROP TABLE houses
        """
    )