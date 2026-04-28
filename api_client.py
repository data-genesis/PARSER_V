import aiohttp
from typing import Any, Optional
from config import config
from utils.logger import setup_logger

logger = setup_logger("api_client")


class PremiumBonusAPI:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _request(self, method: str, endpoint: str, json_data: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }
        session = await self._get_session()
        async with session.request(method, url, headers=headers, json=json_data) as resp:
            data = await resp.json()
            logger.info(f"[{method}] {endpoint} -> {resp.status}")
            return data

    async def buyer_register(
        self,
        phone: str,
        external_id: str,
        name: Optional[str] = None,
        surname: Optional[str] = None,
    ) -> dict:
        payload: dict[str, Any] = {
            "phone": phone,
            "external_id": external_id,
        }
        if name:
            payload["name"] = name
        if surname:
            payload["surname"] = surname
        return await self._request("POST", "/buyer-register", payload)

    async def buyer_info_by_external_id(self, external_id: str) -> dict:
        payload = {
            "external_id": external_id,
        }
        return await self._request("POST", "/buyer-info", payload)

    async def activate_promocode(self, phone: str, code: str) -> dict:
        payload = {
            "phone": phone,
            "code": code,
        }
        return await self._request("POST", "/promocode/activate-promocode", payload)

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()


api = PremiumBonusAPI(config.PB_BASE_URL, config.PB_API_TOKEN)

