"""empty message

Revision ID: 35a1cf4e5a60
Revises: 500d7818ef8f
Create Date: 2017-06-26 02:38:18.306461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35a1cf4e5a60'
down_revision = '500d7818ef8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###
