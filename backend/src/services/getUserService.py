from datetime import datetime
from fastapi import Depends
from loguru import logger
from src.config.db import get_db
from src.models.Role import Role
from src.models.User import User
from src.schemas.user_schema import ReceivedUser, UserDTO
from sqlalchemy.orm import Session

def insert_or_fetch_user(ret_user: ReceivedUser, db: Session = Depends(get_db)):

    # Parsing OHR ID from preferred username
    ohr_id_parsed = str(ret_user.preferred_username.split('@')[0])  
    existing_user = db.query(User).filter(User.ohr_id == ohr_id_parsed).first()  
    
    logger.info(f"Existing user: {existing_user}")
    
    if existing_user:  
        # If the user already exists, simply return the existing user details
        existing_user_dto = UserDTO(**existing_user.model_dump())
        existing_user_dto.is_admin = "User"  

        return {"status": 200, "message": "User already exists", "data": [existing_user_dto.model_dump()]}  
    
    else:  
        # Only create new user if role_id is 1 (treated as "User")
        logger.info("Creating new user")
        
        # Constructing new user details
        user_name = f"{ret_user.given_name} {ret_user.family_name}"  
        new_user = User(  
            email_id=ret_user.email,  
            username=user_name,  
            last_login_time=datetime.now(),  
            created_on=datetime.now(),
            password=None,  # assuming password is handled elsewhere
            role_id=1,  # Always assigning role_id 1 ("User")
            firstname=ret_user.given_name,  
            lastname=ret_user.family_name,  
            ohr_id=ohr_id_parsed  
        )  
        user_dto = UserDTO(**new_user.model_dump())
        user_dto.is_admin = "User"  
        
        db.add(new_user)  
        db.commit()  

        return {"status": 200, "message": "Success", "data": [user_dto.model_dump()]}