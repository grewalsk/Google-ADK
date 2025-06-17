"""Prometheus metrics for monitoring system performance.

Provides comprehensive metrics collection for all components of the
Kalshi trading system using Prometheus client library.
"""

from prometheus_client import Counter, Gauge, Histogram, start_http_server
from loguru import logger

from kalshi_trader.core.config import Settings


class MetricsCollector:
    """Centralized metrics collection using Prometheus."""

    def __init__(self, settings: Settings) -> None:
        """Initialize metrics collector with Prometheus metrics."""
        self.settings = settings
        
        # region System Metrics
        self.orders_total = Counter("kalshi_orders_total", "Total orders placed", ["status"])
        self.portfolio_value = Gauge("kalshi_portfolio_value", "Current portfolio value")
        self.agent_processing_time = Histogram("kalshi_agent_processing_seconds", "Agent processing time", ["agent"])
        # endregion
        
        # region Trading Metrics
        self.pnl_realized = Gauge("kalshi_pnl_realized", "Realized P&L")
        self.pnl_unrealized = Gauge("kalshi_pnl_unrealized", "Unrealized P&L")
        self.active_positions = Gauge("kalshi_active_positions", "Number of active positions")
        # endregion

    def start_metrics_server(self) -> None:
        """Start Prometheus metrics HTTP server."""
        if self.settings.enable_metrics:
            start_http_server(self.settings.prometheus_port)
            logger.info(f"Metrics server started on port {self.settings.prometheus_port}")

    def record_order(self, status: str) -> None:
        """Record order placement."""
        self.orders_total.labels(status=status).inc()

    def update_portfolio_value(self, value: float) -> None:
        """Update current portfolio value."""
        self.portfolio_value.set(value)

    def record_agent_processing_time(self, agent_name: str, duration: float) -> None:
        """Record agent processing duration."""
        self.agent_processing_time.labels(agent=agent_name).observe(duration)


# TODO: Add custom business metrics for trading performance
# TODO: Implement alerting rules for critical metrics
# TODO: Add support for distributed metrics collection 