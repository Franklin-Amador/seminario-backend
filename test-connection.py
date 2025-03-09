import os
from prisma import Prisma

# Print current DATABASE_URL for debugging
print(f"Current DATABASE_URL: {os.environ.get('DATABASE_URL')}")

async def main():
    try:
        # Initialize Prisma client
        print("Initializing Prisma client...")
        prisma = Prisma()
        
        # Connect to the database
        print("Connecting to database...")
        await prisma.connect()
        
        # Test the connection with a simple query
        print("Testing connection with query...")
        # You can replace this with a more appropriate query for your schema
        result = await prisma.raw("SELECT 1 AS test")
        
        print(f"Connection successful! Query result: {result}")
        
        # Disconnect
        await prisma.disconnect()
        print("Disconnected from database")
        
    except Exception as e:
        print(f"Connection error: {str(e)}", )

# Run the async function
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
