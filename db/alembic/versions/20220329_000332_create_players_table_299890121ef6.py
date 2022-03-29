"""create players table

Revision ID: 299890121ef6
Revises: 9b597439f4f8
Create Date: 2022-03-29 00:03:32.356294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '299890121ef6'
down_revision = '9b597439f4f8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('birth_date', sa.Date, nullable=False),
        sa.Column('height_inches', sa.Integer, nullable=False),
        sa.Column('jersey_number', sa.Integer, nullable=False),
        sa.Column('position', sa.String(10), nullable=False),
        sa.Column('team_id', sa.Integer, sa.schema.ForeignKey('teams.id'), nullable=False)
    )


def downgrade():
    op.drop_table('players')
