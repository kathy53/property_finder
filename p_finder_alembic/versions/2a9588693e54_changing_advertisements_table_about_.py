"""changing advertisements table about agent data

Revision ID: 2a9588693e54
Revises: 64743f7119b8
Create Date: 2022-11-24 19:26:38.209851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a9588693e54'
down_revision = '64743f7119b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE advertisements
        DROP COLUMN agent_id;

        ALTER TABLE advertisements
        ADD COLUMN agent_name VARCHAR(150),
        ADD COLUMN agent_membership VARCHAR(200),
        ADD COLUMN agent_url TEXT;
        """
    )


def downgrade() -> None:
    pass
