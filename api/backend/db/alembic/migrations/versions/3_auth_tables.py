from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '3_auth_tables'
down_revision = 'c30c8bbdd23b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- refresh_tokens ---
    op.create_table(
        'refresh_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token_hash', sa.String(255), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default='false'),
    )
    op.create_index('ix_refresh_tokens_token_hash', 'refresh_tokens', ['token_hash'])

    # --- email_verification_tokens ---
    op.create_table(
        'email_verification_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(255), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, server_default='false'),
    )
    op.create_index('ix_email_verification_tokens_token', 'email_verification_tokens', ['token'])

    # --- password_reset_tokens ---
    op.create_table(
        'password_reset_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(255), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, server_default='false'),
    )
    op.create_index('ix_password_reset_tokens_token', 'password_reset_tokens', ['token'])


def downgrade() -> None:
    op.drop_table('password_reset_tokens')
    op.drop_table('email_verification_tokens')
    op.drop_table('refresh_tokens')