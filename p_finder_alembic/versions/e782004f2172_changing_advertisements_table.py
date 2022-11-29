"""changing advertisements table

Revision ID: e782004f2172
Revises: aca0e130e7e9
Create Date: 2022-11-24 18:18:09.215649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e782004f2172'
down_revision = 'aca0e130e7e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE advertisements
        MODIFY property_url VARCHAR(255) NOT NULL PRIMARY KEY;

        ALTER TABLE advertisements
        DROP COLUMN advert_id
        """
    )


def downgrade() -> None:
    pass
