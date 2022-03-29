"""create teams table

Revision ID: 9b597439f4f8
Revises: f813e278aff9
Create Date: 2022-03-29 00:01:02.450224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b597439f4f8'
down_revision = 'f813e278aff9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('city', sa.String(50), nullable=False),
        sa.Column('nickname', sa.String(50), nullable=False),
        sa.Column('code', sa.String(10), nullable=False),
        sa.Column('division_id', sa.Integer, sa.schema.ForeignKey('divisions.id'), nullable=False)
    )


def downgrade():
    op.drop_table('teams')
