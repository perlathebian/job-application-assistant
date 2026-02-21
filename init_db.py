import asyncio
from backend.services.database_service import db_service

async def main():
    await db_service.init_db()
    print("Database initialized!")

if __name__ == "__main__":
    asyncio.run(main())