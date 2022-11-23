"""houses_advert_connection_table

Revision ID: aca0e130e7e9
Revises: 7b6c224f7894
Create Date: 2022-11-22 20:45:46.348197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca0e130e7e9'
down_revision = '7b6c224f7894'
branch_labels = None
depends_on = None

#Table to connect between the houses and advertisements tables 

def upgrade() -> None:
    op.execute(
        """CREATE TABLE houses_advertisements_connection(
           house_id INTEGER,
           advert_id INTEGER
        )"""
    )


def downgrade() -> None:
    op.execute(
        """DROP TABLE houses_advertisements_connection
        """
    )
