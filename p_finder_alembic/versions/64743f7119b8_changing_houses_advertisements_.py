"""changing houses_advertisements_connection table

Revision ID: 64743f7119b8
Revises: e782004f2172
Create Date: 2022-11-24 18:25:14.520324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64743f7119b8'
down_revision = 'e782004f2172'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        -- ALTER TABLE houses_advertisements_connection RENAME COLUMN advert_id TO property_url;
        ALTER TABLE houses_advertisements_connection CHANGE advert_id property_url VARCHAR(255);
        """
    )


def downgrade() -> None:
    pass
