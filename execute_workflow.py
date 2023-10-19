import json
from workflows import NotifyOrder  # 引入工作流
from temporalio.client import Client
import asyncio
from temporalio.api.enums.v1 import WorkflowIdReusePolicy


async def main():
    client = await Client.connect("10.43.12.80:7233",namespace="default")
    await client.get_workflow_handle("order-workflow").terminate()

    # 这里模拟从前端接收到的 JSON
    workflow_json = '''
    {
      "workflow": "NotifyOrder",
      "trigger": "NewOrder",
      "conditions": [
        {
          "field": "amount",
          "operator": ">",
          "value": 20
        }
      ],
      "actions": [
        {
          "activity": "send_email",
          "parameters": {
            "recipient": "admin@example.com",
            "subject": "New Order",
            "content": "You have a new order."
          }
        }
      ]
    }
    '''

    workflow_data = json.loads(workflow_json)
    
    # 根据触发器和条件来决定是否执行工作流
    if workflow_data['trigger'] == 'NewOrder':
        conditions = workflow_data['conditions']
        for condition in conditions:
            if condition['field'] == 'amount' and condition['operator'] == '>' and condition['value'] == 20:
                result = await client.execute_workflow(
                    NotifyOrder.run,
                    25, 
                    id="order-workflow", 
                    task_queue="order-task-queue"
                )
                print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
