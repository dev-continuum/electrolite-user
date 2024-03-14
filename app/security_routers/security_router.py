from utility.custom_logger import logger
from .. import get_db, get_sns, session, google_sso, facebook_sso, get_s3
from fastapi import HTTPException, Depends, status, APIRouter, File, UploadFile
from utility import forms
from fastapi.security import OAuth2PasswordRequestForm
from utility.secret_manager import get_aws_secret
from data_store.data_schemas import *
from wallet_service.wallet_service import ReadUserWalletBalance, CreateInitialOrderId, AddUserWalletBalance
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from app.user_login_regisration_workflows.register_new_user import RegisterUser, RegisterSocialUser
from app.user_login_regisration_workflows.login_existing_user import LoginExistingUser, LoginSocialMediaUser, \
    LogoutExistingUser
from app.user_login_regisration_workflows.check_current_user import get_current_active_user
from app.user_login_regisration_workflows.token_generator import TokenGenerator
from app.user_operations.profile_operations import ProfileOperations
from app.user_operations.vehicle_related_operations import VehicleMake, VehicleModel, RegisterVehicleOperations
from app.user_operations.booking_reservation_operations import UserBookingReservationOperations
from app.user_operations.rate_station import RateStations

oauth_secrets = get_aws_secret(session, "oauth_data")
router = APIRouter()

# to get a string like this run:
# openssl rand-hex 32
SECRET_KEY = oauth_secrets["oauth_key"]
ALGORITHM = oauth_secrets["oauth_algo"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(oauth_secrets["token_expiry"])


@router.post("/signup/otp", response_model=UserResponseModel)
async def otp_for_first_time_user(current_user: FirstTimeUser, db=Depends(get_db), sns=Depends(get_sns)):
    db_operations = UserRelatedDbOperations(db)
    new_user = RegisterUser(current_user=current_user, db_operation=db_operations, sns=sns)
    try:
        response = await new_user.otp_for_first_time_user()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.post("/login/otp", response_model=UserResponseModel)
async def otp_for_user(current_user: User, db=Depends(get_db), sns=Depends(get_sns)):
    db_operations = UserRelatedDbOperations(db)
    login_user = LoginExistingUser(current_user=current_user, db_operation=db_operations, sns=sns)
    try:
        response = await login_user.login_existing_user_through_otp()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.post("/logout", response_model=UserResponseModel)
async def logout_current_user(current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    db_operations = UserRelatedDbOperations(db)
    logout_user = LogoutExistingUser(current_user=current_user, db_operation=db_operations)
    try:
        response = await logout_user.logout_user()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.post("/social/signup")
async def social_signup(data_to_onboard: SocialMediaSignupData, db=Depends(get_db)):
    db_operations = UserRelatedDbOperations(db)
    current_user = User.parse_obj({"phonenumber": data_to_onboard.id})

    try:
        login_user = LoginSocialMediaUser(current_user=current_user, db_operation=db_operations,
                                          access_toke_expiry_time=ACCESS_TOKEN_EXPIRE_MINUTES, algorithm=ALGORITHM,
                                          secret_key=SECRET_KEY)
        logged_in_user = await login_user.login_existing_user_through_social()

    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            try:
                new_user_entry = InitSocialUser(
                    **{"phonenumber": data_to_onboard.id, "email": data_to_onboard.email,
                       "username": data_to_onboard.display_name,
                       "provider": data_to_onboard.provider, "is_active": True})
                signup_user = RegisterSocialUser(current_user=new_user_entry, db_operation=db_operations,
                                                 access_toke_expiry_time=ACCESS_TOKEN_EXPIRE_MINUTES,
                                                 algorithm=ALGORITHM,
                                                 secret_key=SECRET_KEY
                                                 )
                registered_user = await signup_user.create_new_social_user()
            except HTTPException as e:
                return {"status_code": e.status_code, "message": e.detail,
                        "data": {}}
            else:
                return registered_user
        else:
            return {"status_code": e.status_code, "message": e.detail,
                    "data": {}}
    else:
        return logged_in_user


@router.post("/authtoken", response_model=UserResponseModel)
async def login_for_access_token(form_data: forms.CustomPasswordRequestForm = Depends(), db=Depends(get_db)):
    db_operations = UserRelatedDbOperations(db)
    user_data = UserToken.parse_obj({"phonenumber": form_data.phonenumber, "otp": form_data.otp})
    token_generator = TokenGenerator(user_token_data=user_data, db_operation=db_operations,
                                     access_toke_expiry_time=ACCESS_TOKEN_EXPIRE_MINUTES, algorithm=ALGORITHM,
                                     secret_key=SECRET_KEY)
    try:
        result = await token_generator.generate_token()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return result


@router.post("/token", response_model=TokenResponseModel)
async def internal_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """
    this is an internal method only to use with swagger
    """
    converted_form_data = forms.CustomPasswordRequestForm(phonenumber=form_data.username, otp=form_data.password)
    token_response = await login_for_access_token(converted_form_data, db)
    token_response.update({"access_token": token_response["data"]["access_token"]})
    return token_response


@router.get("/get/profile", response_model=UserResponseModel)
async def get_user_profile(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        profile_operations = ProfileOperations(current_user, db_operations=db_operations)
        user_profile = await profile_operations.get_profile()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail, "data": {}}
    else:
        return user_profile


@router.post("/set/image", response_model=UserResponseModel)
async def set_image(image_file: Optional[UploadFile] = File(...), db=Depends(get_db),
                    current_user: User = Depends(get_current_active_user), s3_client=Depends(get_s3)):
    try:
        image_content = await image_file.read()
        db_operations = UserRelatedDbOperations(db=db)
        profile_operations = ProfileOperations(current_user, db_operations=db_operations)
        response = await profile_operations.set_image(image_content, s3_client)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail, "data": {}}
    else:
        return response


@router.post("/set/profile", response_model=UserResponseModel)
async def set_user_profile(user_data: UpdateProfileData, db=Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        profile_operations = ProfileOperations(current_user, db_operations=db_operations)
        response = await profile_operations.set_profile(user_data)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail, "data": {}}
    else:
        return response


@router.post("/register/mail", response_model=UserResponseModel)
async def register_new_user(registered_user: RegisteredUser, db=Depends(get_db),
                            current_user: User = Depends(get_current_active_user)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        profile_operations = ProfileOperations(current_user, db_operations=db_operations)
        response = await profile_operations.set_profile(registered_user)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail, "data": {}}
    else:
        return {"status_code": status.HTTP_201_CREATED, "message": f"username and email registered",
                "data": {"email": registered_user.email,
                         "first_name": registered_user.first_name,
                         "last_name": registered_user.last_name}}


@router.get("/vehicle/make", response_model=UserResponseModel)
def vehicle_make(vehicle_type: str, current_user: User = Depends(get_current_active_user)):
    vehicle_make_data = VehicleMake(vehicle_type=vehicle_type)
    return {"status_code": status.HTTP_201_CREATED, "message": f"Providing vehicle options",
            "data": vehicle_make_data.get_list_of_make()}


@router.get("/vehicle/model", response_model=UserResponseModel)
def vehicle_model(vehicle_type: str, vehicle_make: str, current_user: User = Depends(get_current_active_user)):
    vehicle_options_data = VehicleModel(vehicle_type=vehicle_type, vehicle_make=vehicle_make)
    return {"status_code": status.HTTP_201_CREATED, "message": f"Providing vehicle options",
            "data": vehicle_options_data.get_list_of_models()}


@router.post("/register/vehicle", response_model=UserResponseModel)
async def vehicle_details(register_new_vehicle: RegisterNewVehicle, db=Depends(get_db),
                          current_user: User = Depends(get_current_active_user)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        register_vehicle = RegisterVehicleOperations(current_user=current_user,
                                                     db_operation=db_operations)
        response = await register_vehicle.add_vehicle_for_current_user(register_new_vehicle)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.get("/list/vehicle", response_model=UserResponseModel)
async def get_list_of_vehicles(current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        register_vehicle = RegisterVehicleOperations(current_user=current_user,
                                                     db_operation=db_operations)
        response = await register_vehicle.get_list_of_vehicles_for_current_user()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.post("/remove/vehicle", response_model=UserResponseModel)
async def remove_vehicle_from_list(vehicle_data: RegisterNewVehicle,
                                   current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        register_vehicle = RegisterVehicleOperations(current_user=current_user,
                                                     db_operation=db_operations)
        response = await register_vehicle.remove_vehicle(vehicle_data)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.post("/edit/vehicle", response_model=UserResponseModel)
async def edit_vehicle_for_current_user(old_vehicle_data: RegisterNewVehicle, edited_vehicle_data: RegisterNewVehicle,
                                        current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        register_vehicle = RegisterVehicleOperations(current_user=current_user,
                                                     db_operation=db_operations)
        response = await register_vehicle.edit_vehicle(old_vehicle_data, edited_vehicle_data)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.get("/history", response_model=UserResponseModel)
async def user_booking_history(current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        user_booking_reservation = UserBookingReservationOperations(current_user=current_user,
                                                                    db_operations=db_operations)
        response = await user_booking_reservation.get_transactions()
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.post("/rate/station", response_model=UserResponseModel)
def rate_a_station(station_rating_data: RatingStationData,
                   current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    try:
        db_operations = UserRelatedDbOperations(db=db)
        rating_operations = RateStations(current_user=current_user, db_operations=db_operations)
        response = rating_operations.add_rating_for_a_station(station_rating_data=station_rating_data)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail,
                "data": {}}
    else:
        return response


@router.get("/wallet/balance", response_model=UserResponseModel)
def wallet_details(current_user: User = Depends(get_current_active_user)):
    # read latest wallet balance with transactions details
    return_response = ReadUserWalletBalance(user_id=current_user.phonenumber).read_wallet_data_for_given_user()
    return return_response


@router.post("/wallet/add", response_model=UserResponseModel)
def add_amount_to_user_wallet(data_to_add_balance: TotalDataForTransactionUpdate,
                              current_user: User = Depends(get_current_active_user)):
    data_to_add_balance.user_id = current_user.phonenumber
    return_response = AddUserWalletBalance(data_to_add_balance).update_wallet_details_for_user()
    return return_response


@router.post("/order", response_model=UserResponseModel)
def wallet_details(order_data: OrderDataSchemaToSend, current_user: User = Depends(get_current_active_user)):
    logger.info(f"data to create order id is {order_data}")
    order_data.user_id = current_user.phonenumber
    return_response = CreateInitialOrderId(order_data).get_razorpay_order_for_given_amount()
    return return_response
