"""AudioRecords model update

Revision ID: 71a82776788a
Revises: 2f34c090cdda
Create Date: 2023-08-27 19:42:27.632847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71a82776788a'
down_revision: Union[str, None] = '2f34c090cdda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('audiorecords', 'audio_note',
               existing_type=sa.VARCHAR(length=1000),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('audiorecords', 'audio_note',
               existing_type=sa.VARCHAR(length=1000),
               nullable=False)
    # ### end Alembic commands ###
