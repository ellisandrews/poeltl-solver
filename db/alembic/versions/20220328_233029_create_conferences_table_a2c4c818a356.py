"""create conferences table

Revision ID: a2c4c818a356
Revises: 
Create Date: 2022-03-28 23:30:29.746621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c4c818a356'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'conferences',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(10), nullable=False)
    )


def downgrade():
    op.drop_table('conferences')
