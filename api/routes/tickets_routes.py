from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_ticket_service
from services.ticket_service import TicketService
from models.ticket import Ticket, TicketStatus
from schemas.ticket_schema import TicketCreate, TicketResponse, TicketUpdateStatus, MensagemResponse



router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

def ticket_para_response(ticket:Ticket) -> TicketResponse:
    return TicketResponse(
        id=ticket.id,
        titulo=ticket.titulo,
        descricao=ticket.descricao,
        status=ticket.status.value
    )


@router.get("", response_model=list[TicketResponse])
def listar_tickets(
    status: TicketStatus | None = None,
    limit: int | None = None,
    offset: int = 0,
    service: TicketService = Depends(get_ticket_service)
) -> list[TicketResponse]:
    
    tickets = service.listar_tickets(
        status=status,
        limit=limit,
        offset=offset
    )

    return [ticket_para_response(ticket) for ticket in tickets]

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    responses={
        404 : {
            "description": "Ticket não encontrado."
        }
    }
)
def buscar_ticket(
    ticket_id:int,
    service: TicketService = Depends(get_ticket_service)
) -> TicketResponse:
    ticket = service.buscar_ticket_por_id(ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket não encontrado."
        )
    
    return ticket_para_response(ticket)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
    responses={
        400 : {
            "description": "Dados inválidos para criação do ticket."
        }
    }
)
def criar_ticket(
    dados:TicketCreate,
    service: TicketService = Depends(get_ticket_service)
) -> TicketResponse:
    ticket, resultado = service.criar_ticket(
        titulo=dados.titulo,
        descricao=dados.descricao
    )

    if not resultado.sucesso or ticket is None:
        raise HTTPException(
            status_code=400,
            detail=resultado.mensagem
        )

    return ticket_para_response(ticket)

@router.patch(
    "/{ticket_id}/status",
    response_model=MensagemResponse,
    responses= {
        400 : {
            "description" : "Status inválido ou alteração não permitida."
        },
        404 : {
            "description" : "Ticket não encontrado."
        }
    }
)
def alterar_status_ticket(
    ticket_id:int,
    dados:TicketUpdateStatus,
    service: TicketService = Depends(get_ticket_service)
) -> MensagemResponse:
    resultado = service.alterar_status(
        ticket_id,
        novo_status=dados.status
    )

    if not resultado.sucesso:
        if resultado.mensagem == "Ticket não encontrado.":
            raise HTTPException(
                status_code=404,
                detail=resultado.mensagem
            )

        raise HTTPException(
            status_code=400,
            detail=resultado.mensagem
        )

    return MensagemResponse(
        mensagem=resultado.mensagem
    )

@router.delete(
    "/{ticket_id}",
    response_model=MensagemResponse,
    responses= {
        200 : {
            "description" : "Ticket removido com sucesso."
        },
        404 : {
            "description" : "Não foi possível encontrar o ticket."
        }
    }
)
def deletar_ticket(
    ticket_id: int,
    service: TicketService = Depends(get_ticket_service)
) -> MensagemResponse:
    resultado = service.deletar(ticket_id)
    if not resultado.sucesso:
        raise HTTPException(
            status_code=404,
            detail=resultado.mensagem
        )
    return MensagemResponse(
        mensagem=resultado.mensagem
    )