from utility.custom_logger import logger
from data_store import data_schemas
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from utility.secret_manager import get_aws_secret
from .. import session, get_db

oauth_secrets = get_aws_secret(session, "oauth_data")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = oauth_secrets["oauth_key"]
ALGORITHM = oauth_secrets["oauth_algo"]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user_data(db, user_extracted_from_token):
    db_operation = UserRelatedDbOperations(db)
    try:
        current_user_data = await db_operation.get_user(user_extracted_from_token)
    except HTTPException:
        raise credentials_exception
    else:
        return current_user_data


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """
    :param token:
    :param db:
    It parses the jwt token. If it is valid, tries to fetch user details from db
    :return: User fetched from database
    """

    try:
        logger.debug("decoding user token for authentication")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phonenumber: str = payload.get("sub")
        if phonenumber is None:
            logger.debug("phone number is none raising exception")
            raise credentials_exception
        user_extracted_from_token = data_schemas.UserToken(phonenumber=phonenumber)
    except JWTError:
        logger.exception("exception in decoding the token")
        raise credentials_exception
    else:
        return await get_current_user_data(db, user_extracted_from_token)


async def get_current_active_user(current_user: data_schemas.InitUser = Depends(get_current_user)):
    if not current_user.is_active:
        logger.debug(f"current user {current_user.phonenumber} is not active")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is logged out. Login first")
    return current_user
