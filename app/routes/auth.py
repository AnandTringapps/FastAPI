# from fastapi import FastAPI,Depends, HTTPException,status
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel
# from datetime import timedelta, datetime
# from jose import JWTError, jwt
# from passlib.crypto import CryptoContext

# SECRET_KEY ="de7d629fda5cf5f25c6c638d62caa390a49a94f7b1447449a87f4e7855b3bcb8"
# ALGORITHM ="MS256"
# ACCESS_TOKEN_EXPIRE=30

# emp={
#     "Anand":{
#         "username":"Anand",
#         "hashed_password":"",
#         "email":"anand@mail.com",
#         "disable":True
#     }
# }

# class Token(BaseModel):
#     access_token=str
#     token_type=str

# class TokenData(BaseModel):
#     username:str or None = None

# class User(BaseModel):
#     username:str or None=None
#     email:str or None = None
#     disabled:bool

# class UserInDb(User):
#     hashed_password :str


# pwd_context = CryptoContext(schemes=["bcrypt"], deprecated="auto")
# oauth_2_scheme=OAuth2PasswordBearer(tokenUrl="token")

# app=FastAPI('')

# def verify_password(plain_password, hased_password):
#     return pwd_context.verify(plain_password, hased_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(emp,username:str):
#     if username in emp:
#         user_data = emp[username]
#         return UserInDb(**user_data)
    
# def authenticate_user(emp, username: str,password:str):
#     user= get_user(emp,username)
#     if not user:
#         return False
#     if not verify_password(password,user.hashed_password):
#         return False
    
# def create_access_token(data:dict,expires_delta:timedelta or None=None):
#     to_encode =data.copy()
#     if expires_delta:
#         expire= datetime.utcnow()+expires_delta
#     else:
#         expire=datetime.utcnow()+timedelta(minutes=15)

#     to_encode.update({"exp":expire})
#     encoded_jwt = jwt.encode(to_encode,SECRET_KEY,alogo=ALGORITHM)
#     return encoded_jwt

