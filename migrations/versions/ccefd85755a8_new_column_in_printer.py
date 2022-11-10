"""New column in Printer

Revision ID: ccefd85755a8
Revises: 0f8eccc6e219
Create Date: 2022-11-01 18:04:01.159444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccefd85755a8'
down_revision = '0f8eccc6e219'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('printer', sa.Column('learning_campus', sa.String(length=25), nullable=False))
    op.add_column('printer', sa.Column('cabinet', sa.String(length=10), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('printer', 'cabinet')
    op.drop_column('printer', 'learning_campus')
    # ### end Alembic commands ###
