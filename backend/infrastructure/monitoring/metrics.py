"""
This module contains custom metrics for the monitoring stack.
"""
from opentelemetry import metrics

from settings import settings


meter = metrics.get_meter(name=settings.service_name)

websocket_hub_active_connections = meter.create_up_down_counter(
    name='websocket_hub_active_connections',
    description='The amount of active connections to the websocket hub.',
)
