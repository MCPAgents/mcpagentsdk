class MCPAgentError(Exception):
    """Base exception for MCPAgency."""
    pass

class ConnectionError(MCPAgentError):
    """Raised when there is a connection issue."""
    pass

class ResourceError(MCPAgentError):
    """Raised when there is an issue with resource handling."""
    pass

class ToolError(MCPAgentError):
    """Raised when there is an issue with tool execution."""
    pass
