"""agent_connection_table

Revision ID: a3ff7e89ca95
Revises: f63b07e0ebf7
Create Date: 2022-11-22 20:00:54.861577

Table to connect between the houses and agents tables 
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ff7e89ca95'
down_revision = 'f63b07e0ebf7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """CREATE TABLE houses_agents_conection(
           house_id INTEGER,
           agent_id INTEGER
        )"""
    )


def downgrade() -> None:
    op.execute(
        """DROP TABLE houses_agents_conection"""
    )
