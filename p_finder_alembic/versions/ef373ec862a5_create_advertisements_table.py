"""create advertisements table

Revision ID: ef373ec862a5
Revises: 
Create Date: 2023-11-15 18:16:39.647624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef373ec862a5'
down_revision = None
branch_labels = None
depends_on = None

"""In this table we store all propaganda from all sources, in this case from lamudi
Be aware in the future, as crawling more websites the table columns will increase. This table represents all of our raw data in a 
structured way. """
def upgrade() -> None:
    op.execute(
        """CREATE TABLE advertisements(
            advertisement_id VARCHAR(255) NOT NULL, 
            source VARCHAR(100),
            title TEXT,
            property_url VARCHAR(255),
            location VARCHAR(255),
            description TEXT,
            raw_price TEXT,
            price TEXT,
            coin VARCHAR(255),
            details_item TEXT,
            place_features TEXT,
            facilities TEXT,
            image_url TEXT,
            latitude NUMERIC(9,6),
            longitude NUMERIC(9,6),
            province TEXT,
            locality TEXT,
            district TEXT,
            address TEXT,
            surroundings TEXT,
            publication_date TEXT,
            crawling_date DATE,
            publisher_id VARCHAR(255),
            PRIMARY KEY (advertisement_id) 
        )"""
    )

def downgrade() -> None:
    op.execute(
        """DROP TABLE advertisements """
    )
