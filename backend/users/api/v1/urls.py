from rest_framework.routers import SimpleRouter
from .views import HistoryView, UserView

router = SimpleRouter()

router.register("history", HistoryView, basename="history")
router.register("users", UserView, basename="users")

