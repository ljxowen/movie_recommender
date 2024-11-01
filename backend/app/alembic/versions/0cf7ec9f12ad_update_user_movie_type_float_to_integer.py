"""update user_movie type Float to Integer

Revision ID: 0cf7ec9f12ad
Revises: a722a35fe1d8
Create Date: 2024-09-07 01:13:47.586732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0cf7ec9f12ad'
down_revision: Union[str, None] = 'a722a35fe1d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usermovie', 'movies',
               existing_type=postgresql.ARRAY(sa.DOUBLE_PRECISION(precision=53)),
               type_=sa.ARRAY(sa.Integer()),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usermovie', 'movies',
               existing_type=sa.ARRAY(sa.Integer()),
               type_=postgresql.ARRAY(sa.DOUBLE_PRECISION(precision=53)),
               existing_nullable=True)
    # ### end Alembic commands ###
