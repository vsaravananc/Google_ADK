from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel
import os
from google.adk.models.lite_llm import LiteLlm

nvidia_model = LiteLlm(
    model="nvidia_nim/openai/gpt-oss-20b",
    api_key=os.environ["NVIDIA_NIM_API_KEY"],
)

Agent.set_default_model(nvidia_model)

class UserDetail(BaseModel):
    name: str
    age: int
    current_order: int
    address: str

class OrderDetail(BaseModel):
    order_id: int | None
    delivery_address: str
    food: list[str]
    total_amount: int
    currency: str

class RiderInfo(BaseModel):
    rider_name: str
    rider_phone: str
    country_code: str

class DeliverDetail(BaseModel):
    order_id: int | None
    delivery_address: str
    food: list[str]
    total_amount: int
    currency: str
    order_status: str
    assigned_rider: RiderInfo

def get_user_details(name: str| None) -> dict: 
    """ Retrieves the user details for specified user.

    Args:
        name (str) : The name of the user (eg : saravanan , kumar).
    
    Returns:
        dict : The dictionary contains the user details.
    """
    return {
        'name': 'saravanan',
        'age':24,
        'current_order': 10024,
        'address':'home'
    }

customer_agent = Agent(
    name='customer_agent',
    description='A helpfull assistance to get the specific user.',
    output_schema=UserDetail,
    output_key='user_detail',
    tools=[get_user_details],
)

def get_sepcific_order(order_id: int| None) -> dict:
    "This tool help you to get specific order based on the {order_id}, you can use current_order as order_id"
    return {
        'order_id': order_id,
        'delivery_address':'home',
        'food':['dosa','idly','briyani'],
        'total_amount': 200,
        'currency':'INR',
    }

order_agent = Agent(
    name='order_agent',
    description='A helpfull assistance to get the specific order.',
    output_schema=OrderDetail,
    output_key='order_detail',
    tools=[get_sepcific_order],
)

def get_deliver_status(order_id : int | None) -> dict:
    "This tool help you to get specific order status and delivery patner details based on the {order_id}"
    return {
        'order_id': order_id,
        'delivery_address':'home',
        'food':['dosa','idly','briyani'],
        'total_amount': 200,
        'currency':'INR',
        'order_status': 'on_the_way',
        'assigned_rider': {
            'rider_name':'kumar',
            'rider_phone':'*******187',
            'country_code': '+91',
        }
    }

deliver_agent = Agent(
    name='deliver_agent',
    description="A helpfull assistance to get the specific deliver status.",
    output_schema=DeliverDetail,
    output_key="derliver_detail",
    tools=[get_deliver_status]
)

conculsion_agent = Agent(
    name='conclusion_agent',
    description='A helpfull assistance to answer based on {user_detail},{order_detail} and {derliver_detail}',
    instruction="""
    The ouput should be:-
        describe what the user order
        describe which rider assigned for delivery
        describe the order status.
    """
)

sequential_Agent = SequentialAgent(
    name="order_manager",
    sub_agents=[
        customer_agent,
        order_agent,
        deliver_agent,
        conculsion_agent
    ],
    description=
    """ A helpfull assistance to track the customer order status.

    SCOPES:
        You can track the user order and check the assigned delivery patner and order food item.

    RULES:
        Use your team only for user request about the orders.
        if the user just say 'hi' , just reply with greetings don't use your team.
        Never call tools unnecessarily.
        If you can answer directly, answer directly.
    
    RESPONSIBLITY:
        your responsibility what comes under the scope, if the user is out of the scope, 
        just politely say "hey i can help on your order, checking the assigned derlivery patner detail, order status."
    
    TEAMS AND USECASE:
        You can use you'r team to get order status
        use {customer_agent} to get the user details,
        use {order_agent} to get the current order detail based on the user detail,
        use {deliver_agent} to get the order status and delivery patner detail.
        use {conculsion_agent} for the final response.
    """
)

root_agent = sequential_Agent