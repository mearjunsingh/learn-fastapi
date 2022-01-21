"""more column in posts

Revision ID: dd847f9c4667
Revises: c919e5393088
Create Date: 2022-01-22 03:19:20.722976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd847f9c4667'
down_revision = 'c919e5393088'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
