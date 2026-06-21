from repositories.ticket_postgres_repository import TicketPostgresRepository
from services.ticket_service import TicketService

def get_ticket_service() -> TicketService:
    repo = TicketPostgresRepository()
    return TicketService(repo)