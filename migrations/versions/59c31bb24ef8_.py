"""empty message

Revision ID: 59c31bb24ef8
Revises: 
Create Date: 2023-06-13 00:05:34.057084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c31bb24ef8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tributos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('district', sa.Integer(), nullable=False),
    sa.Column('total_points', sa.Integer(), nullable=False, default=0),
    sa.Column('img_src', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('img_src', name = 'c_img_src'),
    sa.UniqueConstraint('name', name = 'c_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tributos')
    # ### end Alembic commands ###