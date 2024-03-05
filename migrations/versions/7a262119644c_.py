"""empty message

Revision ID: 7a262119644c
Revises: 46747d99fd88
Create Date: 2024-03-05 18:21:00.085418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a262119644c'
down_revision = '46747d99fd88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AllHistory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reason_to_disregard', sa.String(length=512), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AllHistory', schema=None) as batch_op:
        batch_op.drop_column('reason_to_disregard')

    # ### end Alembic commands ###