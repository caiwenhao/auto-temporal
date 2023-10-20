from datetime import timedelta
from temporalio import workflow, activity
from activities import HttpRequestParams  # 引入HttpRequestParams dataclass

# 假设您有一个活动注册表，用于查找活动函数
activity_registry = {
    'http_request_activity': activity.http_request_activity,
    'send_email': activity.send_email_activity  # 添加send_email活动
}

@workflow.defn
class AbstractWorkflow:
    @workflow.run
    async def run(self, config):
        trigger = config.get('trigger')
        conditions = config.get('conditions', [])
        actions = config.get('actions', [])
        
        if not self.check_trigger(trigger):
            return "Trigger conditions not met."
        
        if not all(self.check_condition(c) for c in conditions):
            return "Global conditions not met."
        
        for i, action in enumerate(actions):
            action_conditions = action.get('pre_conditions', [])
            if not all(self.check_condition(c) for c in action_conditions):
                continue
            
            await self.execute_action(action)
            
            action_post_conditions = action.get('post_conditions', [])
            if not all(self.check_condition(c) for c in action_post_conditions):
                break

    def check_trigger(self, trigger):
        return True

    def check_condition(self, condition):
        return True

    async def execute_action(self, action):
        activity_type = action.get('activity')
        parameters = action.get('parameters', {})
        
        activity_fn = activity_registry.get(activity_type)
        if activity_fn:
            if activity_type == 'http_request_activity':
                params = HttpRequestParams(**parameters)  # 使用dataclass封装参数
            else:
                params = parameters  # 其他活动可能不需要dataclass封装

            await workflow.execute_activity(
                activity_fn,
                params,
                start_to_close_timeout=timedelta(seconds=5)
            )
        else:
            print(f"Activity {activity_type} not found.")
