from dataclasses import dataclass

@dataclass
class ResultadoOperacao:
    sucesso: bool
    mensagem: str