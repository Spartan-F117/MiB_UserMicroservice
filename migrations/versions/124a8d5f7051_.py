"""empty message

Revision ID: 124a8d5f7051
Revises: 
Create Date: 2021-11-12 13:38:18.031320

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import PrimaryKeyConstraint


# revision identifiers, used by Alembic.
revision = '124a8d5f7051'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.Unicode(length=128), nullable=False),
    sa.Column('firstname', sa.Unicode(length=128)),
    sa.Column('lastname', sa.Unicode(length=128)),
    sa.Column('password', sa.Unicode(length=128)),
    sa.Column('date_of_birth', sa.Date()),
    sa.Column('location', sa.Unicode(length=128)),
    sa.Column('nickname', sa.Unicode(length=128)),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.Column('lottery_points', sa.Integer()),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('blacklist',
                    sa.Column('id', sa.Integer(), autoincrement=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('blacklisted_user_id', sa.Integer(), nullable=False)
                    )

    op.create_table('reportlist',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('reportlisted_user_id', sa.Integer(), nullable=False)
                    )

    op.create_table('filter',
    sa.Column('user_id',sa.Integer(), primary_key=True, nullable=False),
    sa.Column('list', sa.Unicode(128), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    op.drop_table('filter')
    # ### end Alembic commands ###
