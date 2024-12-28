"""add Note, Tag

Revision ID: 14cb113a0ec0
Revises: 20731bb0d408
Create Date: 2024-12-28 14:56:28.460693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14cb113a0ec0'
down_revision: Union[str, None] = '20731bb0d408'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Note',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=36), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('memo_date', sa.String(length=8), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Note_user_id'), 'Note', ['user_id'], unique=False)
    op.create_table('Tag',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Note_Tag',
    sa.Column('note_id', sa.String(length=36), nullable=True),
    sa.Column('tag_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['note_id'], ['Note.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Note_Tag')
    op.drop_table('Tag')
    op.drop_index(op.f('ix_Note_user_id'), table_name='Note')
    op.drop_table('Note')
    # ### end Alembic commands ###
