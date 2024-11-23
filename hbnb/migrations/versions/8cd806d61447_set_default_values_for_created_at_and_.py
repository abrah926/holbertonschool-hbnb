"""Add created_at and updated_at columns to places table

Revision ID: 8cd806d61447
Revises: bfa670f6bc70
Create Date: 2024-11-23 09:55:22.895243

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8cd806d61447'
down_revision = 'bfa670f6bc70'
branch_labels = None
depends_on = None


def upgrade():
    # Add 'created_at' and 'updated_at' columns to 'places' table
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'created_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP')
        ))
        batch_op.add_column(sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text(
                'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
        ))


def downgrade():
    # Remove 'created_at' and 'updated_at' columns from 'places' table
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('updated_at')
