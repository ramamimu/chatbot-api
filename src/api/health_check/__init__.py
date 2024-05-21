from src.api.health_check.handler import HealthCheckHandler
from src.api.health_check.routes import routes

def register():
  return routes(HealthCheckHandler)