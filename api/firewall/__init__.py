from logging import getLogger


logger = getLogger('firewall')
__all__ = ['logger']
default_app_config = 'firewall.apps.FirewallConfig'
