"""init

Revision ID: 59b064289f6f
Revises: 
Create Date: 2021-10-28 15:51:50.486074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59b064289f6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String, nullable=False),
        sa.Column('hash', sa.String, nullable=False),
        sa.Column('telegram_id', sa.String, nullable=True)
    )


def downgrade():
    op.drop_table('users')
