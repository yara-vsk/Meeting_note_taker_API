from src.api.items import router as router_items
from src.api.meetings import router as router_meetings
from src.api.users import auth_router

all_routers = [
    router_meetings,
    router_items,
    auth_router,
]