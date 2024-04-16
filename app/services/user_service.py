from app.schemas.user_schema import UserAuth, UserOut, FollowSchema
from beanie.odm.operators.update.array import Pull
from fastapi import Depends, status, HTTPException, Header, Response
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from app.models.user_model import Users
from app.core.config import settings
from app.core.security import get_password, verify_password, verify_access_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_str}/login")

class UserService:
    
    @staticmethod
    async def create_user(userData : UserAuth):
       
        
        userData.hashed_password = get_password(password=userData.hashed_password)
        user_in = Users(**userData.model_dump())
        
        await user_in.insert()
        
        return user_in
    
    @staticmethod
    async def authenticate(name: str, passkey: str):
        user = await Users.find_one(Users.username == name)
        
        if not user:
            return None
        if not verify_password(password=passkey, hashed_password = user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def get_current_user( access_token : str = Depends(oauth2_schema)):
        credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})
        
        
        token_data:dict = verify_access_token(access_token, credentialException)
        

        user = await Users.find_one(Users.username == token_data.get("username")).project(FollowSchema)
        
        return user
        
    @staticmethod
    async def follow_user(userId : UUID, current_user):
        user_who_will_follow = await Users.find_one(Users.username == current_user.username)
        follow_user = await Users.find_one(Users.user_id == userId)

        # print(current_user.username)
        # print(follow_user.model_dump().get('user_id'))

        follower_dict = follow_user.model_dump()
        user_who_will_follow_dict = user_who_will_follow.model_dump()


        follower_data = FollowSchema(user_id=follower_dict.get('user_id'), username=follower_dict.get('username'), email = follower_dict.get('email'), profile_pic= follower_dict.get('profile_pic'))

        user_who_will_follow_data = FollowSchema(user_id=user_who_will_follow_dict.get('user_id'), username=user_who_will_follow_dict.get('username'), email = user_who_will_follow_dict.get('email'), profile_pic= user_who_will_follow_dict.get('profile_pic'))

        count = 0 
        following_list = user_who_will_follow.following

        for index in range(0, len(following_list)):

            if following_list[index].user_id == userId:
                count+=1

            if count == 1:
                user_who_will_follow.following.pop(index)
                await user_who_will_follow.save()
                follow_user.followers.remove(user_who_will_follow_data)
                await follow_user.save()
                return "unfollowing operation successful!"
                # ind = following_list.index(user)
                # print(ind)
                # user_following.following.pop(ind)
                # await user_following.save()

                
                

        if count == 0 : 
            follow_user.followers.append(user_who_will_follow_data)
            await follow_user.save()
            user_who_will_follow.following.append(follower_data)
            await user_who_will_follow.save()
            return "following operation successfull!"
