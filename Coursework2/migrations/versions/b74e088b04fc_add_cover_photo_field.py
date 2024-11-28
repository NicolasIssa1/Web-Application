"""Add cover photo field

Revision ID: b74e088b04fc
Revises: 1297e3cfb1ac
Create Date: 2024-11-27 23:28:09.108750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b74e088b04fc'
down_revision = '1297e3cfb1ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cover_photo', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('linkedin', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('github', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('twitter', sa.String(length=250), nullable=True))
        batch_op.drop_column('security_question')
        batch_op.drop_column('security_answer')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('security_answer', sa.VARCHAR(length=100), server_default=sa.text("'Default Answer'"), nullable=False))
        batch_op.add_column(sa.Column('security_question', sa.VARCHAR(length=150), server_default=sa.text("'Default Question'"), nullable=False))
        batch_op.drop_column('twitter')
        batch_op.drop_column('github')
        batch_op.drop_column('linkedin')
        batch_op.drop_column('cover_photo')

    op.drop_table('like')
    op.drop_table('comment')
    # ### end Alembic commands ###