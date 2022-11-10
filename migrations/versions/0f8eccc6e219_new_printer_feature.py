"""New printer feature

Revision ID: 0f8eccc6e219
Revises: 
Create Date: 2022-10-30 17:02:28.710846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f8eccc6e219'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Issuance')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Issuance',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=15), nullable=True),
    sa.Column('learning_campus', sa.VARCHAR(length=35), nullable=True),
    sa.Column('cabinet', sa.VARCHAR(length=15), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('user', sa.VARCHAR(length=40), nullable=True),
    sa.Column('cartridge_number_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['cartridge_number_id'], ['cartridges.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
