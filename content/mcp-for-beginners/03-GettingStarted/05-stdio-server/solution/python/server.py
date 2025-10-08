#!/usr/bin/env python3
"""
MCP stdio server example - Updated for MCP Specification 2025-06-18

This server demonstrates the recommended stdio transport instead of the 
deprecated SSE transport. The stdio transport is simpler, more secure,
and provides better performance.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Configure logging to stderr (never use stdout for logging in stdio servers)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create the server
server = Server("example-stdio-server")

@server.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    result = a + b
    logger.info(f"Adding {a} + {b} = {result}")
    return result

@server.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together"""
    result = a * b
    logger.info(f"Multiplying {a} * {b} = {result}")
    return result

@server.tool()
def get_greeting(name: str) -> str:
    """Generate a personalized greeting"""
    greeting = f"Hello, {name}! Welcome to the MCP stdio server."
    logger.info(f"Generated greeting for {name}")
    return greeting

@server.tool()
def get_server_info() -> dict:
    """Get information about this MCP server"""
    return {
        "server_name": "example-stdio-server",
        "version": "1.0.0",
        "transport": "stdio",
        "capabilities": ["tools"],
        "description": "Example MCP server using stdio transport (MCP 2025-06-18 specification)"
    }

async def main():
    """Main server function using stdio transport"""
    logger.info("Starting MCP stdio server...")
    
    try:
        # Use stdio transport - this is the recommended approach
        async with stdio_server(server) as (read_stream, write_stream):
            logger.info("Server connected via stdio transport")
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
