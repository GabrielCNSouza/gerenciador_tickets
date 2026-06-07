from pydantic import BaseModel


from models.tickets_status import TicketStatus

class TicketResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str

class TicketCreate(BaseModel):
    titulo: str
    descricao: str

class TicketUpdateStatus(BaseModel):
    status: TicketStatus