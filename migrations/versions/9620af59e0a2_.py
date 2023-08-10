"""empty message

Revision ID: 9620af59e0a2
Revises: 1f745d308677
Create Date: 2023-08-04 20:02:24.928342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9620af59e0a2'
down_revision = '1f745d308677'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###