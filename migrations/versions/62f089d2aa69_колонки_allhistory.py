"""+ колонки allhistory

Revision ID: 62f089d2aa69
Revises: 50609ad96891
Create Date: 2023-05-07 21:03:54.536806

"""
from alembic import op
import sqlalchemy as sa
from script import main_func


# revision identifiers, used by Alembic.
revision = '62f089d2aa69'
down_revision = '8a0af0a31178'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AllHistory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('learning_campus', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('cabinet', sa.String(length=20), nullable=True))
    main_func()

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AllHistory', schema=None) as batch_op:
        batch_op.drop_column('cabinet')
        batch_op.drop_column('learning_campus')
        batch_op.drop_column('location')
        batch_op.drop_column('status')

    # ### end Alembic commands ###
