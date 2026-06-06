from models.ticket import Ticket
from models.tickets_status import TicketStatus
from services.ticket_service import TicketService
from repositories.ticket_postgres_repository import TicketPostgresRepository



def exibir_menu() -> None:
    print('\n--- Gerenciador de Tickets ---\n')
    print(' 1.Criar ticket')
    print(' 2.Listar tickets')
    print(' 3.Buscar ticket por ID')
    print(' 4.Alterar o status do ticket')
    print(' 0.Sair')

def exibir_ticket(ticket: Ticket) -> None:
    print(f'ID: {ticket.id}')
    print(f'Título: {ticket.titulo}')
    print(f'Descrição: {ticket.descricao}')
    print(f'Status: {ticket.status.value}')
    print('-'*30)

def criar_ticket(service: TicketService) -> None:
    titulo = input('Título: ').strip()
    descricao = input('Descrição: ').strip()
    
    _, resultado = service.criar_ticket(titulo=titulo, descricao=descricao)

    print(resultado.mensagem)
    

def listar_tickets(service: TicketService) -> None:
    tickets = service.listar_tickets()
    if not tickets:
        print('Nenhum ticket cadastrado.')
        return
    
    for ticket in tickets:
        exibir_ticket(ticket)


def buscar_ticket(service: TicketService) -> None:
    entrada = input('Digite o ID do ticket: ').strip()

    if not entrada.isdigit():
        print('ID inválido. Digite apenas números.')
        return
    
    ticket_id = int(entrada)

    ticket = service.buscar_ticket_por_id(ticket_id)

    if ticket is None:
        print('Ticket não encontrado.')
        return

    print('\n----- Ticket encontrado -----')
    exibir_ticket(ticket)


def alterar_status_ticket(service: TicketService) -> None:
    entrada = input('Digite o ID do ticket: ').strip()

    if not entrada.isdigit():
        print('ID inválido. Digite apenas números.')
        return

    ticket_id = int(entrada)

    ticket = service.buscar_ticket_por_id(ticket_id)

    if ticket is None:
        print('Ticket não encontrado.')
        return
    
    print(f'\nStatus atual do ticket: {ticket.status.value}')

    print('\nStatus disponíveis:')
    print('1. aberto')
    print('2. em andamento')
    print('3. fechado')

    opcao_status = input('Escolha o novo status: ').strip()

    if opcao_status == '1':
        novo_status = TicketStatus.ABERTO
    elif opcao_status == '2':
        novo_status = TicketStatus.EM_ANDAMENTO
    elif opcao_status == '3':
        novo_status = TicketStatus.FECHADO
    else:
        print('Status inválido.')
        return

    resultado = service.alterar_status(ticket_id, novo_status)

    print(resultado.mensagem)


def main() -> None:

    repo = TicketPostgresRepository()
    service = TicketService(repo)

    while True:

        exibir_menu()
        opcao = input('-> ').strip().lower()

        if opcao == '0':
            print('Programa encerrado.')
            break

        if opcao == '1':
            criar_ticket(service)  
        elif opcao == '2':
            listar_tickets(service)
        elif opcao == '3':
            buscar_ticket(service)
        elif opcao == '4':
            alterar_status_ticket(service)
        else:
            print('Opção inválida.')

if __name__ == "__main__":
    main()
    