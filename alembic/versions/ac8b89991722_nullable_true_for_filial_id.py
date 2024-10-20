"""nullable true for filial_id

Revision ID: ac8b89991722
Revises: 1e3f11cd783a
Create Date: 2024-09-05 14:58:29.985073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac8b89991722'
down_revision: Union[str, None] = '1e3f11cd783a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_id', table_name='user')
    op.drop_table('user')
    op.alter_column('employees', 'filial_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('employees', 'filial_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(length=1024), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    # ### end Alembic commands ###
