"""create publishers table

Revision ID: 1db7b0834228
Revises: ef373ec862a5
Create Date: 2023-11-15 20:46:35.050739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1db7b0834228'
down_revision = 'ef373ec862a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """CREATE TABLE real_estate_entity(
            publisher_id VARCHAR(255) NOT NULL, 
            publisher TEXT,
            agency TEXT,
            publisher_url TEXT,
            agency_url TEXT,
            publisher_phone TEXT,
            PRIMARY KEY (publisher_id) 
        )"""
    )


def downgrade() -> None:
    op.execute(
        """DROP TABLE real_estate_entity """
    )
