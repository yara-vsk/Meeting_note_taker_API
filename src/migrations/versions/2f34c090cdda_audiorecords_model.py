"""AudioRecords model

Revision ID: 2f34c090cdda
Revises: 1ae80e2d538b
Create Date: 2023-08-27 18:22:49.201180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f34c090cdda'
down_revision: Union[str, None] = '1ae80e2d538b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audiorecords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=500), nullable=False),
    sa.Column('audio_note', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file_name')
    )
    op.add_column('items', sa.Column('audio_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'items', 'audiorecords', ['audio_id'], ['id'])
    op.drop_column('items', 'audio_note')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('audio_note', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.drop_column('items', 'audio_id')
    op.drop_table('audiorecords')
    # ### end Alembic commands ###
