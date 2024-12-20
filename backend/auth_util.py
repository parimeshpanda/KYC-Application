
from fastapi import Request
from fastapi.responses import JSONResponse
from okta_jwt_verifier import JWTVerifier
from starlette.middleware.base import BaseHTTPMiddleware
from src.constants import Constant

class OktaJWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        OKTA_ISSUER = Constant.ISSUER
        OKTA_CLIENT_ID = Constant.CLIENT_ID

        accessToken = request.headers.get("authorization", None)

        if accessToken is not None:
            try:
                accessToken = accessToken.split(" ")[1]
                jwt_verifier = JWTVerifier(OKTA_ISSUER, OKTA_CLIENT_ID, "api://default")
                await jwt_verifier.verify_access_token(accessToken)
                return await call_next(request)
            except Exception as e:
                return JSONResponse({"error": f"Unauthorized token or {e}"}, status_code=401)
        else:
            return JSONResponse({"error": "Unauthorized Access"}, status_code=401)