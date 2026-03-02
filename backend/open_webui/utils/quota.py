from datetime import datetime
from sqlalchemy.orm import Session
from open_webui.models.daily_usage import DailyUsage

DAILY_LIMIT = 10

def check_and_increase_quota(db: Session, user):

    # 👑 admin 無限制
    if user.role == "admin":
        return True

    today = datetime.utcnow().strftime("%Y-%m-%d")

    usage = db.query(DailyUsage).filter_by(
        user_id=user.id,
        date=today
    ).first()

    if usage and usage.count >= DAILY_LIMIT:
        return False

    if usage:
        usage.count += 1
    else:
        usage = DailyUsage(
            user_id=user.id,
            date=today,
            count=1
        )
        db.add(usage)

    db.commit()
    return True
