"""add due_date and tags

Revision ID: add_due_date_and_tags
Revises: 9f722de76c9e
Create Date: 2026-02-23 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_due_date_and_tags'
down_revision: Union[str, Sequence[str], None] = '9f722de76c9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tags table
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)
    
    # Create todo_tags association table
    op.create_table('todo_tags',
    sa.Column('todo_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['todo_id'], ['todos.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('todo_id', 'tag_id')
    )
    
    # Add due_date column to todos
    op.add_column('todos', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_todos_due_date'), 'todos', ['due_date'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop due_date column
    op.drop_index(op.f('ix_todos_due_date'), table_name='todos')
    op.drop_column('todos', 'due_date')
    
    # Drop todo_tags table
    op.drop_table('todo_tags')
    
    # Drop tags table
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
