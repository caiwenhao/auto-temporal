import json
from temporalio.client import Client
import asyncio
from workflows import AbstractWorkflow

async def main():
    client = await Client.connect("192.168.66.174:7233", namespace="default")
    #await client.get_workflow_handle("order-workflow").terminate()

    workflow_json = '''
    {
      "workflow": "AbstractWorkflow",
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

    result = await client.execute_workflow(
        AbstractWorkflow.run,
        workflow_data,
        id="order-workflow-03",
        task_queue="order-task-queue"
    )
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
