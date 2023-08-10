"""empty message

Revision ID: 1f745d308677
Revises: da49b86b376c
Create Date: 2023-08-03 12:37:00.802723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f745d308677'
down_revision = 'da49b86b376c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association2',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('building_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['building_id'], ['Buildings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association2')
    # ### end Alembic commands ###