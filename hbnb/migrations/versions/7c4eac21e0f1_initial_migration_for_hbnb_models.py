"""Initial migration for HBnB models

Revision ID: 7c4eac21e0f1
Revises: 
Create Date: 2024-11-22 12:29:15.644820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c4eac21e0f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('amenities',
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('first_name', sa.String(
                        length=128), nullable=False),
                    sa.Column('last_name', sa.String(
                        length=128), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=False),
                    sa.Column('password_hash', sa.String(
                        length=256), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('places',
                    sa.Column('title', sa.String(length=128), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.Column('latitude', sa.Float(), nullable=False),
                    sa.Column('longitude', sa.Float(), nullable=False),
                    sa.Column('owner_id', sa.String(
                        length=36), nullable=False),
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('place_amenities',
                    sa.Column('place_id', sa.String(
                        length=36), nullable=False),
                    sa.Column('amenity_id', sa.String(
                        length=36), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['amenity_id'], ['amenities.id'], ),
                    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
                    sa.PrimaryKeyConstraint('place_id', 'amenity_id')
                    )
    op.create_table('reviews',
                    sa.Column('text', sa.Text(), nullable=False),
                    sa.Column('rating', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.String(length=36), nullable=False),
                    sa.Column('place_id', sa.String(
                        length=36), nullable=False),
                    sa.Column('id', sa.String(length=36), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('place_amenities')
    op.drop_table('places')
    op.drop_table('users')
    op.drop_table('amenities')
    # ### end Alembic commands ###