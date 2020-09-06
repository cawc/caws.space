"""add urls with click counting

Revision ID: aadd5bfa88ce
Revises: 
Create Date: 2020-09-07 00:06:57.120722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aadd5bfa88ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URL',
    sa.Column('token', sa.String(length=128), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('URL')
    # ### end Alembic commands ###
