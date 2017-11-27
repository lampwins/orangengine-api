from __future__ import unicode_literals

from rest_framework import routers

from . import views


class FirewallRootView(routers.APIRootView):
    """
    Firewall API root view
    """
    def get_view_name(self):
        return 'Firewall'


router = routers.DefaultRouter()
router.APIRootView = FirewallRootView

# Field choices
router.register(r'_choices', views.FirewallFieldChoicesViewSet, base_name='field-choice')

# Firewalls
router.register(r'firewalls', views.FirewallViewSet)

app_name = 'firewall-api'
urlpatterns = router.urls
