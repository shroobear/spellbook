"""Add character_class column to character

Revision ID: 943b9b76d586
Revises: bc66399bf3b3
Create Date: 2023-08-14 00:12:44.964101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '943b9b76d586'
down_revision: Union[str, None] = 'bc66399bf3b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('character_class', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('character', 'character_class')
    # ### end Alembic commands ###