"""houses_adds_table

Revision ID: 7b6c224f7894
Revises: a3ff7e89ca95
Create Date: 2022-11-22 20:07:19.497767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b6c224f7894'
down_revision = 'a3ff7e89ca95'
branch_labels = None
depends_on = None

"""In this table we store all propaganda i.e. from all sources (lamudi, viva anuncios, etcetera)
Be aware in the future, as crawling more websites the table columns will increase. This table represents all of our raw data in a 
structured way. """
def upgrade() -> None:
    op.execute(
        """CREATE TABLE advertisements(
            advert_id INTEGER, 
            source VARCHAR(100),
            title TEXT,
            property_url VARCHAR(255),
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
            agent_id INTEGER,
            crawling_date DATE
        )"""
    )


def downgrade() -> None:
    op.execute(
        """DROP TABLE advertisements"""
    )