"""удаление колонки dn в User

Revision ID: 50609ad96891
Revises: f6f0c3fafff6
Create Date: 2023-04-26 19:18:25.784690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50609ad96891'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_column('dn')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dn', sa.VARCHAR(length=50), nullable=False))

    # ### end Alembic commands ###
