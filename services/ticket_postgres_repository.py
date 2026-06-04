from database import conectar
from models.ticket import Ticket
from models.tickets_status import TicketStatus
from models.resultado_alteracao_status import ResultadoAlteracaoStatus



class TicketPostgresRepository:

    def listar(self) -> list[Ticket]:
        tickets = []

        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        t.id,
                        t.titulo,
                        t.descricao,
                        s.nome AS status
                    FROM tickets AS t
                    INNER JOIN ticket_status AS s
                        ON t.status_id = s.id
                    ORDER BY t.id;
                """)
                linhas = cursor.fetchall()
                for linha in linhas:
                    ticket = Ticket(
                        id=linha[0],
                        titulo=linha[1],
                        descricao=linha[2],
                        status=TicketStatus(linha[3])
                    )
                    tickets.append(ticket)

        return tickets
    
    def buscar_por_id(self, ticket_id: int) -> Ticket | None:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        t.id,
                        t.titulo,
                        t.descricao,
                        s.nome AS status
                    FROM tickets AS t
                    INNER JOIN ticket_status AS s
                        ON t.status_id = s.id
                    WHERE t.id = %s;
                    """,
                    (ticket_id,)
                )

                linha = cursor.fetchone()

        if not linha:
            return None
        
        return Ticket(
            id=linha[0],
            titulo=linha[1],
            descricao=linha[2],
            status=TicketStatus(linha[3])
        )
    
    def criar(self, titulo: str, descricao: str) -> Ticket | None:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tickets (titulo, descricao, status_id)
                    VALUES (
                        %s,
                        %s,
                        (
                            SELECT id
                            FROM ticket_status
                            WHERE nome = %s
                        )
                    )
                    RETURNING id;
                    """,
                    (titulo, descricao, TicketStatus.ABERTO.value)
                )

                linha = cursor.fetchone()

        if not linha:
            return None
        
        return Ticket(
            id=linha[0],
            titulo=titulo,
            descricao=descricao,
            status=TicketStatus.ABERTO
        )
    
    def alterar_status(self, ticket_id: int, novo_status: TicketStatus) -> ResultadoAlteracaoStatus:
        ticket = self.buscar_por_id(ticket_id)

        if not ticket:
            return ResultadoAlteracaoStatus(sucesso=False)
        
        status_antigo = ticket.status

        if status_antigo == novo_status:
            return ResultadoAlteracaoStatus(
                sucesso=True,
                status_antigo=status_antigo,
                status_novo=novo_status
            )
        
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tickets
                    SET status_id = (
                        SELECT id
                        FROM ticket_status
                        WHERE nome = %s
                    )
                    WHERE id = %s
                    """,
                    (novo_status.value, ticket_id)
                )
        return ResultadoAlteracaoStatus(
            sucesso=True,
            status_antigo=status_antigo,
            status_novo=novo_status
        )