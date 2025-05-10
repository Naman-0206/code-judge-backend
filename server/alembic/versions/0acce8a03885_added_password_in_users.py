"""added password in users

Revision ID: 0acce8a03885
Revises: 166d1cdc31e8
Create Date: 2025-05-10 22:04:38.087417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '0acce8a03885'
down_revision: Union[str, None] = '166d1cdc31e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing foreign key constraints
    op.drop_constraint('questions_creator_id_fkey', 'questions', type_='foreignkey')
    op.drop_constraint('submissions_creator_id_fkey', 'submissions', type_='foreignkey')

    # Alter columns
    op.alter_column('users', 'id',
        existing_type=sa.CHAR(length=32),
        type_=sa.String(),
        existing_nullable=False
    )
    op.alter_column('questions', 'creator_id',
        existing_type=sa.CHAR(length=32),
        type_=sa.String(),
        existing_nullable=False
    )
    op.alter_column('submissions', 'creator_id',
        existing_type=sa.CHAR(length=32),
        type_=sa.String(),
        existing_nullable=False
    )

    # Add new columns to users
    op.add_column('users', sa.Column('updated_at', sa.DateTime(),
        server_default=func.now(),   # default for existing rows
        onupdate=func.now(),         # auto-update on modification (SQLAlchemy ORM only)
        nullable=False
    ))
    op.add_column('users', sa.Column('password', sa.String(length=100), nullable=False, server_default='password'))

    # Recreate foreign key constraints
    op.create_foreign_key('questions_creator_id_fkey', 'questions', 'users', ['creator_id'], ['id'])
    op.create_foreign_key('submissions_creator_id_fkey', 'submissions', 'users', ['creator_id'], ['id'])


def downgrade() -> None:
    # Drop new foreign key constraints
    op.drop_constraint('questions_creator_id_fkey', 'questions', type_='foreignkey')
    op.drop_constraint('submissions_creator_id_fkey', 'submissions', type_='foreignkey')

    # Drop added columns
    op.drop_column('users', 'password')
    op.drop_column('users', 'updated_at')

    # Revert altered columns
    op.alter_column('users', 'id',
        existing_type=sa.String(),
        type_=sa.CHAR(length=32),
        existing_nullable=False
    )
    op.alter_column('questions', 'creator_id',
        existing_type=sa.String(),
        type_=sa.CHAR(length=32),
        existing_nullable=False
    )
    op.alter_column('submissions', 'creator_id',
        existing_type=sa.String(),
        type_=sa.CHAR(length=32),
        existing_nullable=False
    )

    # Recreate original foreign keys
    op.create_foreign_key('questions_creator_id_fkey', 'questions', 'users', ['creator_id'], ['id'])
    op.create_foreign_key('submissions_creator_id_fkey', 'submissions', 'users', ['creator_id'], ['id'])
