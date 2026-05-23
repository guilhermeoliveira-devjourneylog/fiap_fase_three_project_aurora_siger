from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List
import heapq


# =========================================================
# ENUMS
# =========================================================

class NivelRisco(Enum):
    BAIXO = "BAIXO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    CRITICO = "CRÍTICO"


class EstadoSistema(Enum):
    NORMAL = "NORMAL"
    ALERTA = "ALERTA"
    CONTINGENCIA = "CONTINGÊNCIA"
    EMERGENCIA = "EMERGÊNCIA"


# =========================================================
# MODELOS
# =========================================================

@dataclass
class EventoOperacional:
    subsistema: str
    valor: float
    limite: float
    timestamp: datetime


# =========================================================
# DECISION ENGINE
# =========================================================

class DecisionEngine:
    """
    Motor responsável por:
    - regras condicionais;
    - priorização;
    - análise de risco;
    - decisões automáticas;
    - acionamento de alertas.
    """

    def __init__(self):

        # ==============================================
        # Estado global da colônia
        # ==============================================
        self.estado_atual = EstadoSistema.NORMAL

        # ==============================================
        # Filas de prioridade (heap)
        # ==============================================
        self.fila_prioridade = []

        # ==============================================
        # Alertas ativos
        # ==============================================
        self.alertas: List[str] = []

        # ==============================================
        # Estados dos subsistemas
        # ==============================================
        self.subsistemas: Dict[str, Dict] = {

            "energia": {
                "estado": "ESTÁVEL",
                "prioridade": 1
            },

            "temperatura": {
                "estado": "NORMAL",
                "prioridade": 2
            },

            "estrutura": {
                "estado": "SEGURA",
                "prioridade": 0
            },

            "comunicacao": {
                "estado": "ONLINE",
                "prioridade": 3
            },

            "suporte_vida": {
                "estado": "ATIVO",
                "prioridade": -1
            }
        }

    # =====================================================
    # ANÁLISE DE RISCO
    # =====================================================

    def analisar_risco(
        self,
        evento: EventoOperacional
    ) -> NivelRisco:
        """
        Analisa risco operacional.
        """

        percentual = (
            evento.valor / evento.limite
        ) * 100

        if percentual < 70:

            risco = NivelRisco.BAIXO

        elif percentual < 90:

            risco = NivelRisco.MODERADO

        elif percentual < 110:

            risco = NivelRisco.ALTO

        else:

            risco = NivelRisco.CRITICO

        print(
            f"[RISCO] "
            f"{evento.subsistema} -> "
            f"{risco.value}"
        )

        return risco

    # =====================================================
    # PRIORIZAÇÃO
    # =====================================================

    def priorizar_subsistemas(self):
        """
        Organiza subsistemas por prioridade.
        """

        print("\n[PRIORIZAÇÃO]\n")

        self.fila_prioridade.clear()

        for nome, dados in self.subsistemas.items():

            prioridade = dados["prioridade"]

            heapq.heappush(
                self.fila_prioridade,
                (prioridade, nome)
            )

        while self.fila_prioridade:

            prioridade, nome = heapq.heappop(
                self.fila_prioridade
            )

            print(
                f"Prioridade {prioridade} "
                f"-> {nome}"
            )

    # =====================================================
    # AUTOMAÇÃO
    # =====================================================

    def executar_automacao(
        self,
        evento: EventoOperacional
    ):
        """
        Executa respostas automáticas.
        """

        print("\n[AUTOMAÇÃO]\n")

        risco = self.analisar_risco(evento)

        # ==========================================
        # TEMPERATURA
        # ==========================================

        if evento.subsistema == "temperatura":

            if risco == NivelRisco.CRITICO:

                self.alertas.append(
                    "RESFRIAMENTO DE EMERGÊNCIA ATIVADO"
                )

                self.subsistemas["temperatura"][
                    "estado"
                ] = "EMERGÊNCIA"

                print(
                    "[AÇÃO] Resfriamento ativado."
                )

        # ==========================================
        # ENERGIA
        # ==========================================

        elif evento.subsistema == "energia":

            if risco in [
                NivelRisco.ALTO,
                NivelRisco.CRITICO
            ]:

                self.alertas.append(
                    "MODO ECONOMIA DE ENERGIA"
                )

                self.subsistemas["energia"][
                    "estado"
                ] = "CONTINGÊNCIA"

                print(
                    "[AÇÃO] Redução de consumo."
                )

        # ==========================================
        # ESTRUTURA
        # ==========================================

        elif evento.subsistema == "estrutura":

            if risco == NivelRisco.CRITICO:

                self.alertas.append(
                    "ISOLAMENTO ESTRUTURAL"
                )

                self.subsistemas["estrutura"][
                    "estado"
                ] = "RISCO CRÍTICO"

                print(
                    "[AÇÃO] Compartimentos isolados."
                )

        # ==========================================
        # SUPORTE DE VIDA
        # ==========================================

        elif evento.subsistema == "suporte_vida":

            if risco != NivelRisco.BAIXO:

                self.alertas.append(
                    "PROTOCOLO DE SOBREVIVÊNCIA"
                )

                self.subsistemas["suporte_vida"][
                    "estado"
                ] = "PROTEÇÃO"

                print(
                    "[AÇÃO] Protocolo ativado."
                )

    # =====================================================
    # ALTERAÇÃO DE ESTADO
    # =====================================================

    def alterar_estado(self):
        """
        Atualiza estado global da colônia.
        """

        print("\n[ALTERAÇÃO DE ESTADO]\n")

        estados_criticos = 0
        estados_alerta = 0

        for nome, dados in self.subsistemas.items():

            estado = dados["estado"]

            print(f"{nome} -> {estado}")

            if (
                "CRÍTICO" in estado
                or "EMERGÊNCIA" in estado
            ):
                estados_criticos += 1

            elif (
                "ALERTA" in estado
                or "CONTINGÊNCIA" in estado
            ):
                estados_alerta += 1

        # ==========================================
        # DECISÃO GLOBAL
        # ==========================================

        if estados_criticos > 0:

            self.estado_atual = (
                EstadoSistema.EMERGENCIA
            )

        elif estados_alerta > 0:

            self.estado_atual = (
                EstadoSistema.CONTINGENCIA
            )

        else:

            self.estado_atual = (
                EstadoSistema.NORMAL
            )

        print(
            f"\nESTADO GLOBAL -> "
            f"{self.estado_atual.value}"
        )

    # =====================================================
    # ALERTAS
    # =====================================================

    def exibir_alertas(self):

        print("\n[ALERTAS ATIVOS]\n")

        if not self.alertas:

            print("Nenhum alerta ativo.")
            return

        for alerta in self.alertas:
            print(alerta)


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

engine = DecisionEngine()

# ==============================================
# EVENTOS
# ==============================================

evento_temp = EventoOperacional(
    subsistema="temperatura",
    valor=118,
    limite=100,
    timestamp=datetime.now()
)

evento_energia = EventoOperacional(
    subsistema="energia",
    valor=92,
    limite=100,
    timestamp=datetime.now()
)

evento_estrutura = EventoOperacional(
    subsistema="estrutura",
    valor=135,
    limite=100,
    timestamp=datetime.now()
)

# ==============================================
# PRIORIZAÇÃO
# ==============================================

engine.priorizar_subsistemas()

# ==============================================
# AUTOMAÇÃO
# ==============================================

engine.executar_automacao(
    evento_temp
)

engine.executar_automacao(
    evento_energia
)

engine.executar_automacao(
    evento_estrutura
)

# ==============================================
# ESTADO GLOBAL
# ==============================================

engine.alterar_estado()

# ==============================================
# ALERTAS
# ==============================================

engine.exibir_alertas()