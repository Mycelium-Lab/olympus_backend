"""init

Revision ID: a66e9b0560e0
Revises: 59b064289f6f
Create Date: 2021-10-28 16:12:12.004057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a66e9b0560e0'
down_revision = '59b064289f6f'
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