from temporalio import activity

@activity.defn
async def send_email(recipient: str) -> str:
    # 执行实际的邮件发送逻辑
    return f"Email sent to {recipient} with subject"
