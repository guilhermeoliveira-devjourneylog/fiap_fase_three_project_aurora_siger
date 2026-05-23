from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List
import heapq


# =========================================================
# ENUMS
# =========================================================

class TipoAlerta(Enum):
    ENERGETICO = "ENERGÉTICO"
    CLIMATICO = "CLIMÁTICO"
    ESTRUTURAL = "ESTRUTURAL"
    OPERACIONAL = "OPERACIONAL"
    CRITICO = "CRÍTICO"


class Severidade(Enum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4


class CanalNotificacao(Enum):
    PAINEL = "PAINEL CENTRAL"
    MOBILE = "DISPOSITIVO MÓVEL"
    RADIO = "RÁDIO OPERACIONAL"
    EMERGENCIA = "SISTEMA DE EMERGÊNCIA"


# =========================================================
# MODELOS
# =========================================================

@dataclass
class Alerta:
    id_alerta: int
    tipo: TipoAlerta
    severidade: Severidade
    mensagem: str
    timestamp: datetime


# =========================================================
# ALERT MANAGER
# =========================================================

class AlertManager:
    """
    Sistema responsável pela comunicação operacional
    da colônia Aurora.

    Responsabilidades:
    - geração de alertas;
    - classificação;
    - notificação operacional;
    - priorização;
    - comunicação emergencial.
    """

    def __init__(self):

        # ==============================================
        # Banco de alertas
        # ==============================================
        self.alertas: List[Alerta] = []

        # ==============================================
        # Fila de prioridade
        # ==============================================
        self.fila_alertas = []

        # ==============================================
        # Operadores registrados
        # ==============================================
        self.operadores = [
            "Operador Alpha",
            "Operador Beta",
            "Supervisor Central"
        ]

        # ==============================================
        # Contador
        # ==============================================
        self.contador_alertas = 0

    # =====================================================
    # GERAÇÃO
    # =====================================================

    def gerar_alerta(
        self,
        tipo: TipoAlerta,
        severidade: Severidade,
        mensagem: str
    ) -> Alerta:
        """
        Gera um novo alerta operacional.
        """

        self.contador_alertas += 1

        alerta = Alerta(
            id_alerta=self.contador_alertas,
            tipo=tipo,
            severidade=severidade,
            mensagem=mensagem,
            timestamp=datetime.now()
        )

        self.alertas.append(alerta)

        # ==========================================
        # Heap de prioridade
        # Menor valor -> maior prioridade
        # ==========================================

        heapq.heappush(
            self.fila_alertas,
            (
                -alerta.severidade.value,
                alerta.id_alerta,
                alerta
            )
        )

        print(
            f"[ALERTA GERADO] "
            f"{alerta.tipo.value} "
            f"- {alerta.mensagem}"
        )

        return alerta

    # =====================================================
    # CLASSIFICAÇÃO
    # =====================================================

    def classificar_alerta(
        self,
        alerta: Alerta
    ) -> str:
        """
        Classifica criticidade operacional.
        """

        print("\n[CLASSIFICAÇÃO]\n")

        if alerta.severidade == Severidade.CRITICA:

            classificacao = (
                "RISCO IMEDIATO À COLÔNIA"
            )

        elif alerta.severidade == Severidade.ALTA:

            classificacao = (
                "RISCO OPERACIONAL ELEVADO"
            )

        elif alerta.severidade == Severidade.MEDIA:

            classificacao = (
                "MONITORAMENTO NECESSÁRIO"
            )

        else:

            classificacao = (
                "EVENTO INFORMATIVO"
            )

        print(
            f"Alerta #{alerta.id_alerta}\n"
            f"Tipo: {alerta.tipo.value}\n"
            f"Classificação: {classificacao}\n"
        )

        return classificacao

    # =====================================================
    # NOTIFICAÇÃO
    # =====================================================

    def notificar_operador(
        self,
        alerta: Alerta
    ):
        """
        Notifica operadores automaticamente.
        """

        print("\n[NOTIFICAÇÃO]\n")

        # ==========================================
        # Seleção do canal
        # ==========================================

        if alerta.severidade == Severidade.CRITICA:

            canal = CanalNotificacao.EMERGENCIA

        elif alerta.severidade == Severidade.ALTA:

            canal = CanalNotificacao.RADIO

        elif alerta.severidade == Severidade.MEDIA:

            canal = CanalNotificacao.MOBILE

        else:

            canal = CanalNotificacao.PAINEL

        for operador in self.operadores:

            print(
                f"Destino: {operador}\n"
                f"Canal: {canal.value}\n"
                f"Mensagem: {alerta.mensagem}\n"
            )

    # =====================================================
    # PROCESSAMENTO
    # =====================================================

    def processar_fila_alertas(self):
        """
        Processa alertas por prioridade.
        """

        print("\n[PROCESSAMENTO DE ALERTAS]\n")

        while self.fila_alertas:

            _, _, alerta = heapq.heappop(
                self.fila_alertas
            )

            self.classificar_alerta(alerta)

            self.notificar_operador(alerta)

    # =====================================================
    # DASHBOARD
    # =====================================================

    def exibir_dashboard(self):

        print("\n[DASHBOARD OPERACIONAL]\n")

        if not self.alertas:

            print("Nenhum alerta ativo.")
            return

        for alerta in self.alertas:

            print(
                f"[{alerta.id_alerta}] "
                f"{alerta.tipo.value} | "
                f"{alerta.severidade.name} | "
                f"{alerta.mensagem}"
            )

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def exibir_estatisticas(self):

        print("\n[ESTATÍSTICAS]\n")

        estatisticas: Dict[str, int] = {}

        for alerta in self.alertas:

            tipo = alerta.tipo.value

            if tipo not in estatisticas:
                estatisticas[tipo] = 0

            estatisticas[tipo] += 1

        for tipo, quantidade in estatisticas.items():

            print(
                f"{tipo}: {quantidade}"
            )


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

manager = AlertManager()

# ==============================================
# ALERTA ENERGÉTICO
# ==============================================

alerta1 = manager.gerar_alerta(
    tipo=TipoAlerta.ENERGETICO,
    severidade=Severidade.ALTA,
    mensagem="Sobrecarga detectada no núcleo solar."
)

# ==============================================
# ALERTA CLIMÁTICO
# ==============================================

alerta2 = manager.gerar_alerta(
    tipo=TipoAlerta.CLIMATICO,
    severidade=Severidade.MEDIA,
    mensagem="Tempestade de areia aproximando-se."
)

# ==============================================
# ALERTA ESTRUTURAL
# ==============================================

alerta3 = manager.gerar_alerta(
    tipo=TipoAlerta.ESTRUTURAL,
    severidade=Severidade.CRITICA,
    mensagem="Falha estrutural detectada no módulo B."
)

# ==============================================
# ALERTA OPERACIONAL
# ==============================================

alerta4 = manager.gerar_alerta(
    tipo=TipoAlerta.OPERACIONAL,
    severidade=Severidade.BAIXA,
    mensagem="Rotina de manutenção agendada."
)

# ==============================================
# PROCESSAMENTO
# ==============================================

manager.processar_fila_alertas()

# ==============================================
# DASHBOARD
# ==============================================

manager.exibir_dashboard()

# ==============================================
# ESTATÍSTICAS
# ==============================================

manager.exibir_estatisticas()