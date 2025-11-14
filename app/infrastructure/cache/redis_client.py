import json
from typing import Optional, Any
import redis.asyncio as redis
from app.core.config import settings


class RedisCache:
    """Cliente Redis para cache."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Conecta ao Redis."""
        self.redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def disconnect(self):
        """Desconecta do Redis."""
        if self.redis_client:
            await self.redis_client.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache."""
        if not self.redis_client:
            await self.connect()
        
        value = await self.redis_client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, expire: int = 3600):
        """Define valor no cache."""
        if not self.redis_client:
            await self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        await self.redis_client.setex(key, expire, value)
    
    async def delete(self, key: str):
        """Remove valor do cache."""
        if not self.redis_client:
            await self.connect()
        
        await self.redis_client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Verifica se chave existe."""
        if not self.redis_client:
            await self.connect()
        
        return bool(await self.redis_client.exists(key))


# Instância global
cache = RedisCache()

