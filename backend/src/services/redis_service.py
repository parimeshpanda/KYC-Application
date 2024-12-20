from datetime import datetime
import json
from typing import Dict, List  
from src.constants import Constant

redis_conn = Constant.REDIS_CONN
  

def datetime_serializer(obj):  
    if isinstance(obj, datetime):  
        return obj.isoformat()  # serialize datetime as ISO string
    raise TypeError("Type not serializable error")  # In case an object is not serializable

def json_serialize(data):  
    return json.dumps(data, default=datetime_serializer)  # Apply datetime serializer globally

# Initialize a conversation with an empty list and set expiry
def initialize_conversation(thread_id: str, ttl=3600):  
    redis_conn.set(thread_id, json_serialize([]))  
    redis_conn.expire(thread_id, ttl) 

# Append new data to the existing conversation in Redis
def append_to_redis(thread_id: str, data: Dict, ttl=3600):  
    existing_conversation = redis_conn.get(thread_id)  
    if existing_conversation:  
        conversation = json.loads(existing_conversation)  
        conversation.append(data["result"])  
    else:  
        conversation = [data["result"]]  
    
    # Re-store the updated conversation and reset TTL
    redis_conn.set(thread_id, json_serialize(conversation))  # Update the conversation
    redis_conn.expire(thread_id, ttl)

# Read conversation from Redis
def read_conversation_from_redis(thread_id: str) -> List[Dict]:  
    conversation = redis_conn.get(thread_id)  
    if conversation:  
        return json.loads(conversation)  
    return []  