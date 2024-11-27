"""Added security question and answer fields

Revision ID: 5784d39823c3
Revises: 1297e3cfb1ac
Create Date: 2024-11-27 03:32:13.452150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5784d39823c3'
down_revision = '1297e3cfb1ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('security_question', sa.String(length=150), nullable=False))
        batch_op.add_column(sa.Column('security_answer', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('security_answer')
        batch_op.drop_column('security_question')

    # ### end Alembic commands ###
