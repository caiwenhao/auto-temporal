from datetime import timedelta
from temporalio import workflow
from activities import send_email  # 引入活动

@workflow.defn
class NotifyOrder:
    @workflow.run
    async def run(self, amount: float) -> str:
        if amount > 20:
            return await workflow.execute_activity(
                send_email, "admin@example.com",start_to_close_timeout=timedelta(seconds=5)
            )
        else:
            return "Order amount too small, no email sent."
