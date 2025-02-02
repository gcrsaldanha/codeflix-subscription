from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakError, KeycloakGetError
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.application.ports.auth_service import AuthService, IAMUser, IAMError


class KeycloakConfig(BaseSettings):
    server_url: str
    admin_username: str
    admin_password: str
    realm_name: str
    client_id: str
    client_secret_key: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix='keycloak_')


class KeycloakAuthService(AuthService):
    def __init__(self, config: KeycloakConfig) -> None:
        self.admin = KeycloakAdmin(
            server_url=config.server_url,
            username=config.admin_username,
            password=config.admin_password,
            realm_name=config.realm_name,
            client_id=config.client_id,
            verify=True,
        )

        self.openid = KeycloakOpenID(
            server_url=config.server_url,
            client_id=config.client_id,
            realm_name=config.realm_name,
            client_secret_key=config.client_secret_key,
        )

    def create_user(self, email: str, password: str) -> IAMUser:
        try:
            user_id = self.admin.create_user(
                {
                    "email": email,
                    "username": email,
                    "enabled": True,
                    "credentials": [
                        {"type": "password", "value": password, "temporary": False}
                    ],
                },
                exist_ok=True,  # Do not raise an error if user already exists
            )
            return IAMUser(
                iam_user_id=user_id,
                email=email,
            )
        except KeycloakError:
            raise IAMError("Error creating user")

    def find_by_email(self, email: str) -> IAMUser | None:
        try:
            users = self.admin.get_users(query={"email": email})
            if users:
                user = users[0]
                return IAMUser(
                    iam_user_id=user["id"],
                    email=user["email"],
                )
        except KeycloakGetError:
            return None

    def verify_token(self, token: str) -> bool:
        try:
            self.openid.introspect(token)
            return True
        except KeycloakError:
            return False
