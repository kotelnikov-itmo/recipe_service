from sqlalchemy import func


def fast_count(q) -> int:
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count
