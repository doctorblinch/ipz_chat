"""Chat fix

Revision ID: 16a9146517ab
Revises: 9dd7fd5dcbc4
Create Date: 2019-05-24 10:46:28.892894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16a9146517ab'
down_revision = '9dd7fd5dcbc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_column('user', 'chat_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('chat_id', sa.INTEGER(), nullable=True))
    op.drop_table('chats_users')
    # ### end Alembic commands ###