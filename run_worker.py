import asyncio
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import AbstractWorkflow  # 引入工作流
import activities

async def main():
    client = await Client.connect("192.168.66.174:7233", namespace="default")
    # 初始化 worker
    worker = Worker(
        client, 
        task_queue="order-task-queue", 
        workflows=[AbstractWorkflow],  # 添加工作流
        activities=[activities.http_request_activity]  # 添加活动
    )

    # 运行 worker，这会使其开始监听任务队列并执行工作流和活动
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
