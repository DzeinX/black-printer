"""empty message

Revision ID: 957fd8d9c801
Revises: 62f089d2aa69
Create Date: 2023-05-13 12:29:33.801328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '957fd8d9c801'
down_revision = '62f089d2aa69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('BroughtAPrinter')
    op.drop_table('BroughtACartridge')
    op.drop_table('CartridgeIssuance')
    op.drop_table('PrinterIssuance')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('PrinterIssuance',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=15), nullable=True),
    sa.Column('learning_campus', sa.VARCHAR(length=35), nullable=True),
    sa.Column('cabinet', sa.VARCHAR(length=15), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('user', sa.VARCHAR(length=40), nullable=True),
    sa.Column('printer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['printer_id'], ['printer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CartridgeIssuance',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=15), nullable=True),
    sa.Column('learning_campus', sa.VARCHAR(length=35), nullable=True),
    sa.Column('cabinet', sa.VARCHAR(length=15), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('user', sa.VARCHAR(length=40), nullable=True),
    sa.Column('cartridge_number_id', sa.INTEGER(), nullable=True),
    sa.Column('printer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['cartridge_number_id'], ['cartridges.id'], ),
    sa.ForeignKeyConstraint(['printer_id'], ['printer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('BroughtACartridge',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=15), nullable=False),
    sa.Column('learning_campus', sa.VARCHAR(length=35), nullable=False),
    sa.Column('cabinet', sa.VARCHAR(length=15), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('user', sa.VARCHAR(length=40), nullable=False),
    sa.Column('cartridge_number_id', sa.INTEGER(), nullable=True),
    sa.Column('printer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['cartridge_number_id'], ['cartridges.id'], ),
    sa.ForeignKeyConstraint(['printer_id'], ['printer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('BroughtAPrinter',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('location', sa.VARCHAR(length=15), nullable=False),
    sa.Column('learning_campus', sa.VARCHAR(length=35), nullable=False),
    sa.Column('cabinet', sa.VARCHAR(length=15), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('user', sa.VARCHAR(length=40), nullable=False),
    sa.Column('printer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['printer_id'], ['printer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
