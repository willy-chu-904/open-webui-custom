from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class RollingLimitMiddleware(BaseHTTPMiddleware):

    store = {}

    async def dispatch(self, request: Request, call_next):

        if request.url.path.startswith("/api/chat"):

            user = request.state.user if hasattr(request.state, "user") else None

            if user:

                # ✅ 1️⃣ Admin 無限制
                if getattr(user, "role", None) == "admin":
                    return await call_next(request)

                user_id = user.id
                now = datetime.now(ZoneInfo("Asia/Hong_Kong"))

                # 如果沒有紀錄 → 建立新視窗
                if user_id not in self.store:
                    self.store[user_id] = {
                        "window_start": now,
                        "count": 0
                    }

                window_start = self.store[user_id]["window_start"]

                # ✅ 2️⃣ 檢查是否超過 6 小時
                if now - window_start >= timedelta(hours=6):
                    self.store[user_id] = {
                        "window_start": now,
                        "count": 0
                    }

                # ✅ 3️⃣ 檢查次數
                if self.store[user_id]["count"] >= 10:
                    raise HTTPException(
                        status_code=403,
                        detail="Limit reached (10 requests per 6 hours)."
                    )

                self.store[user_id]["count"] += 1

        response = await call_next(request)
        return response
