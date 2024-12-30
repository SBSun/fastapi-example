from contextvars import ContextVar

user_context: ContextVar[dict | None] = ContextVar("current_user", default=None)