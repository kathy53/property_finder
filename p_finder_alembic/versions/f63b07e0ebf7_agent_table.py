"""agent_table
Revision ID: f63b07e0ebf7
Revises: b432fa732f73
Create Date: 2022-11-22 12:23:35.968628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f63b07e0ebf7'
down_revision = 'b432fa732f73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """CREATE TABLE agents(
            agent_id INTEGER NOT NULL,
            agent_name VARCHAR(150),
            agent_membership VARCHAR(200),            
            agent_url TEXT
        )"""
    )

def downgrade() -> None:
    op.execute(
        """DROP TABLE agents """
    )
