"""Added THE DIFFERENT mODELS FOR THE FOOD MANAGEMNET SYS

Revision ID: 93e1a5f53d5a
Revises: 36d3c7321f34
Create Date: 2024-03-25 00:48:21.721319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93e1a5f53d5a'
down_revision: Union[str, None] = '36d3c7321f34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bulking_menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cutting_menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('option', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delivery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('street_name', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('bulking_menu_id', sa.Integer(), nullable=True),
    sa.Column('cutting_menu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bulking_menu_id'], ['bulking_menus.id'], ),
    sa.ForeignKeyConstraint(['cutting_menu_id'], ['cutting_menus.id'], ),
    sa.ForeignKeyConstraint(['user_name'], ['users.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('number_of_guests', sa.Integer(), nullable=True),
    sa.Column('deposit_paid', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_name'], ['users.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations')
    op.drop_table('delivery')
    op.drop_table('users')
    op.drop_table('cutting_menus')
    op.drop_table('bulking_menus')
    # ### end Alembic commands ###
