"""create divisions table

Revision ID: f813e278aff9
Revises: a2c4c818a356
Create Date: 2022-03-28 23:51:03.790929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f813e278aff9'
down_revision = 'a2c4c818a356'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'divisions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('abbreviation', sa.String(10), nullable=False),
        sa.Column('conference_id', sa.Integer, sa.schema.ForeignKey('conferences.id'), nullable=False)
    )


def downgrade():
    op.drop_table('divisions')
