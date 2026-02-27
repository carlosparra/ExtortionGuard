from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "numbers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("phone_hash", sa.String(64), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column("last4", sa.String(4), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("phone_hash"),
    )
    op.create_index("ix_numbers_country_hash", "numbers", ["country", "phone_hash"])

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("number_id", sa.Integer, sa.ForeignKey("numbers.id", ondelete="CASCADE")),
        sa.Column("channel", sa.String(8), nullable=False),
        sa.Column("reason", sa.String(64), nullable=False),
        sa.Column("details", sa.Text, nullable=False),
        sa.Column("evidence_url", sa.String(512)),
        sa.Column("reporter_id", sa.String(64)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ip_hash", sa.String(64)),
        sa.Column("is_moderated", sa.Boolean, nullable=False, server_default=sa.text("false")),  # ← here
        sa.Index("ix_reports_number_time", "number_id", "created_at"),
        sa.UniqueConstraint("number_id", "reporter_id", "channel", name="uq_report_once_per_reporter_channel"),
    )

    op.create_table(
        "appeals",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("number_id", sa.Integer, sa.ForeignKey("numbers.id", ondelete="CASCADE")),
        sa.Column("claimant_token", sa.String(64), nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default=sa.text("'open'")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

def downgrade():
    op.drop_table("appeals")
    op.drop_table("reports")
    op.drop_index("ix_numbers_country_hash", table_name="numbers")
    op.drop_table("numbers")
