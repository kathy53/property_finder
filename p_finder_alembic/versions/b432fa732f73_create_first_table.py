"""create first table

Revision ID: b432fa732f73
Revises: 
Create Date: 2022-11-21 17:35:41.912751

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
        """CREATE TABLE probe(
            id_house INTEGER,
            url_banner VARCHAR(250)
        )"""
    )


def downgrade() -> None:
    op.execute(
        """DROP TABLE probe
        """
    )