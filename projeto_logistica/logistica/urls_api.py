from rest_framework.routers import DefaultRouter
from .views_api import *

router = DefaultRouter()
router.register("clientes", ClienteViewSet)
router.register("motoristas", MotoristaViewSet)
router.register("veiculos", VeiculoViewSet)
router.register("entregas", EntregaViewSet)
router.register("rotas", RotaViewSet)

urlpatterns = router.urls