from ninja import NinjaAPI

api = NinjaAPI(title="AI Moderated Blog API")

api.add_router("users/", "custom_users.api.router")
