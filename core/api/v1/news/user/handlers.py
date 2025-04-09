from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router
from ninja.errors import HttpError

from jwt import PyJWTError

from core.api.schemas import ApiResponse, StatusResponse
from core.api.v1.news.user.schemas import ClientSchemaPrivate, TokenOutSchema, LogInSchema, UpdatePwInSchema, \
    TokenClientOutSchema, UpdateEmailInSchema, CredentialsInSchema, SignUpInSchema, ScoreInSchema
from core.apps.common.auth.ninja_auth import jwt_auth
from core.apps.common.exceptions import ServiceException
from core.apps.news.services.user import BaseClientService
from core.apps.news.usecases.user.create import CreateClientUseCase
from core.apps.news.usecases.user.get_info import GetClientInfoUseCase
from core.apps.news.usecases.user.login import LoginClientUseCase
from core.apps.news.usecases.user.logout import LogoutClientUseCase
from core.apps.news.usecases.user.update_access_token import UpdateAccessTokenUseCase
from core.apps.news.usecases.user.update_credentials import UpdateClientCredentialsUseCase
from core.apps.news.usecases.user.update_email import UpdateClientEmailUseCase
from core.apps.news.usecases.user.update_password import UpdateClientPasswordUseCase
from core.apps.news.usecases.user.update_score import UpdateClientScoreUseCase
from core.project.containers.containers import get_container


router = Router(tags=["Client"])


@router.post(
    "sign-up",
    response={201: ApiResponse[ClientSchemaPrivate]},
    operation_id='sign_up',
    auth=jwt_auth,
)
def sign_up(request: HttpRequest, schema: SignUpInSchema) -> ApiResponse[ClientSchemaPrivate]:
    container = get_container()
    use_case: CreateClientUseCase = container.resolve(CreateClientUseCase)
    try:
        client = use_case.execute(
            first_name=schema.first_name,
            last_name=schema.last_name,
            middle_name=schema.middle_name,
            role=schema.role,
            email=schema.email,
            password=schema.password,
            verify_password=schema.verify_password,
        )
    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )

    return ApiResponse(
        data=ClientSchemaPrivate.from_entity(client=client),
    )

@router.get(
    "info",
    response={200: ApiResponse[ClientSchemaPrivate]},
    operation_id='get_client_info',
    auth=jwt_auth,
)
def get_client_info(request: HttpRequest) -> ApiResponse[ClientSchemaPrivate]:
    container = get_container()
    client_service: BaseClientService = container.resolve(BaseClientService)
    use_case: GetClientInfoUseCase = container.resolve(GetClientInfoUseCase)
    try:
        user_email: str = client_service.get_client_email_from_token(token=request.auth)
        client = use_case.execute(user_email)

    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )

    return ApiResponse(
        data=ClientSchemaPrivate.from_entity(client=client),
    )


@router.post(
    "log-in",
    response=ApiResponse[TokenOutSchema],
    operation_id='login',
)
def login(request: HttpRequest, response: HttpResponse, schema: LogInSchema) -> ApiResponse[TokenOutSchema]:
    container = get_container()
    use_case: LoginClientUseCase = container.resolve(LoginClientUseCase)
    try:
        client, jwt_tokens = use_case.execute(email=schema.email, password=schema.password)
        response.set_cookie(key="refresh_token", value=jwt_tokens.refresh_token, httponly=True, samesite="Strict")
    except ServiceException:
        raise HttpError(
            status_code=400,
            message='Invalid email or password',
        )

    return ApiResponse(
        data=TokenOutSchema.from_values(access_token=jwt_tokens.access_token, refresh_token=jwt_tokens.refresh_token),
    )


@router.post(
    "log-out",
    response=ApiResponse[StatusResponse],
    operation_id='logout',
    auth=jwt_auth,
)
def logout(request: HttpRequest, response: HttpResponse) -> ApiResponse[StatusResponse]:
    container = get_container()
    use_case: LogoutClientUseCase = container.resolve(LogoutClientUseCase)
    try:
        use_case.execute(token=request.auth)
        response.delete_cookie(key="refresh_token")
    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )

    return ApiResponse(
        data=StatusResponse(status="Successfully logged out"),
    )


@router.post(
    "update_access_token",
    response=ApiResponse[TokenOutSchema],
    operation_id='update_access_token',
)
def update_access_token(request: HttpRequest) -> ApiResponse[TokenOutSchema]:
    container = get_container()
    use_case: UpdateAccessTokenUseCase = container.resolve(UpdateAccessTokenUseCase)

    try:
        jwt_tokens = use_case.execute(request.COOKIES.get("refresh_token"))
    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )
    except PyJWTError:
        raise HttpError(
            status_code=401,
            message='Invalid token uat',
        )
    return ApiResponse(
        data=TokenOutSchema.from_values(access_token=jwt_tokens.access_token),
    )


@router.patch(
    "update_password",
    response=ApiResponse[StatusResponse],
    operation_id='update_password',
    auth=jwt_auth,
)
def update_password(request: HttpRequest, schema: UpdatePwInSchema) -> ApiResponse[StatusResponse]:
    container = get_container()
    client_service: BaseClientService = container.resolve(BaseClientService)
    use_case: UpdateClientPasswordUseCase = container.resolve(UpdateClientPasswordUseCase)

    try:
        user_email: str = client_service.get_client_email_from_token(token=request.auth)
        use_case.execute(
            email=user_email,
            old_password=schema.old_password,
            new_password=schema.new_password,
            verify_password=schema.verify_password,
        )
    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )

    return ApiResponse(
        data=StatusResponse(
            status="Password updated successfully",
        ),
    )


@router.patch(
    "update_email",
    response=ApiResponse[TokenClientOutSchema],
    operation_id='update_email',
    auth=jwt_auth,
)
def update_email(
        request: HttpRequest,
        response: HttpResponse,
        schema: UpdateEmailInSchema,
) -> ApiResponse[TokenClientOutSchema]:
    container = get_container()
    client_service = container.resolve(BaseClientService)
    use_case: UpdateClientEmailUseCase = container.resolve(UpdateClientEmailUseCase)

    try:
        user_email: str = client_service.get_client_email_from_token(token=request.auth)
        client, jwt_tokens = use_case.execute(
            old_email=user_email,
            new_email=schema.new_email,
            password=schema.password,
        )
        response.set_cookie(key="refresh_token", value=jwt_tokens.refresh_token, httponly=True, samesite="Strict")
    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )
    return ApiResponse(
        data=TokenClientOutSchema.from_entity_with_token_values(client=client, access_token=jwt_tokens.access_token, refresh_token=jwt_tokens.refresh_token),
    )


@router.patch(
    "update_credentials",
    response=ApiResponse[ClientSchemaPrivate],
    operation_id='update_credentials',
    auth=jwt_auth,
)
def update_credentials(request: HttpRequest, schema: CredentialsInSchema) -> ApiResponse[ClientSchemaPrivate]:
    container = get_container()
    client_service: BaseClientService = container.resolve(BaseClientService)
    use_case: UpdateClientCredentialsUseCase = container.resolve(UpdateClientCredentialsUseCase)

    try:
        user_email: str = client_service.get_client_email_from_token(token=request.auth)
        client = use_case.execute(
            email=user_email,
            first_name=schema.first_name,
            last_name=schema.last_name,
            middle_name=schema.middle_name,
        )

    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )
    return ApiResponse(
        data=ClientSchemaPrivate.from_entity(client=client),
    )

@router.patch(
    "update_credentials",
    response=ApiResponse[ClientSchemaPrivate],
    operation_id='update_credentials',
    auth=jwt_auth,
)
def update_credentials(request: HttpRequest, schema: CredentialsInSchema) -> ApiResponse[ClientSchemaPrivate]:
    container = get_container()
    client_service: BaseClientService = container.resolve(BaseClientService)
    use_case: UpdateClientCredentialsUseCase = container.resolve(UpdateClientCredentialsUseCase)

    try:
        user_email: str = client_service.get_client_email_from_token(token=request.auth)
        client = use_case.execute(
            email=user_email,
            first_name=schema.first_name,
            last_name=schema.last_name,
            middle_name=schema.middle_name,
        )

    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )
    return ApiResponse(
        data=ClientSchemaPrivate.from_entity(client=client),
    )

@router.patch(
    "update_score",
    response=ApiResponse[ClientSchemaPrivate],
    operation_id='update_score',
)
def update_credentials(request: HttpRequest, client_email: str, schema: ScoreInSchema) -> ApiResponse[ClientSchemaPrivate]:
    container = get_container()
    use_case: UpdateClientScoreUseCase = container.resolve(UpdateClientScoreUseCase)
    try:
        client = use_case.execute(
            email=client_email,
            liked=schema.liked,
        )

    except ServiceException as e:
        raise HttpError(
            status_code=400,
            message=e.message,
        )
    return ApiResponse(
        data=ClientSchemaPrivate.from_entity(client=client),
    )

@router.post(
    "delete_cookie",
    response=ApiResponse[StatusResponse],
    operation_id='delete_cookie',
)
def delete_cookies(request: HttpRequest, response: HttpResponse) -> ApiResponse[StatusResponse]:
    response.delete_cookie(key="refresh_token")
    return ApiResponse(
        data=StatusResponse(status="Successfully deleted cookie"),
    )
