from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List
import numpy as np


# =========================================================
# MODELOS
# =========================================================

@dataclass
class RegistroEnergetico:
    timestamp: datetime
    geracao_solar: float
    geracao_eolica: float
    consumo: float


# =========================================================
# PREDICTION ENGINE
# =========================================================

class PredictionEngine:
    """
    Camada responsável por:
    - regressão linear;
    - previsão de geração;
    - simulação de cenários;
    - análise preditiva da colônia Aurora.
    """

    def __init__(self):

        # ==============================================
        # Histórico energético
        # ==============================================
        self.historico: List[RegistroEnergetico] = []

        # ==============================================
        # Vetores NumPy
        # ==============================================
        self.vetor_tempo = np.array([])
        self.vetor_geracao_solar = np.array([])
        self.vetor_geracao_eolica = np.array([])
        self.vetor_consumo = np.array([])

        # ==============================================
        # Coeficientes regressão
        # y = ax + b
        # ==============================================
        self.coeficiente_angular = 0.0
        self.coeficiente_linear = 0.0

    # =====================================================
    # REGISTRO
    # =====================================================

    def adicionar_registro(
        self,
        geracao_solar: float,
        geracao_eolica: float,
        consumo: float
    ):

        indice_tempo = len(self.vetor_tempo)

        registro = RegistroEnergetico(
            timestamp=datetime.now(),
            geracao_solar=geracao_solar,
            geracao_eolica=geracao_eolica,
            consumo=consumo
        )

        self.historico.append(registro)

        self.vetor_tempo = np.append(
            self.vetor_tempo,
            indice_tempo
        )

        self.vetor_geracao_solar = np.append(
            self.vetor_geracao_solar,
            geracao_solar
        )

        self.vetor_geracao_eolica = np.append(
            self.vetor_geracao_eolica,
            geracao_eolica
        )

        self.vetor_consumo = np.append(
            self.vetor_consumo,
            consumo
        )

        print(
            f"[REGISTRO] "
            f"Solar={geracao_solar} "
            f"Eólica={geracao_eolica}"
        )

    # =====================================================
    # REGRESSÃO LINEAR
    # =====================================================

    def executar_regressao_linear(self):
        """
        Executa regressão linear simples.
        """

        print("\n[REGRESSÃO LINEAR]\n")

        if len(self.vetor_tempo) < 2:

            print(
                "Dados insuficientes "
                "para regressão."
            )

            return

        # ==========================================
        # Modelo linear:
        # y = ax + b
        # ==========================================

        coeficientes = np.polyfit(
            self.vetor_tempo,
            self.vetor_geracao_solar,
            1
        )

        self.coeficiente_angular = coeficientes[0]
        self.coeficiente_linear = coeficientes[1]

        print(
            f"Coeficiente angular: "
            f"{self.coeficiente_angular:.4f}"
        )

        print(
            f"Coeficiente linear: "
            f"{self.coeficiente_linear:.4f}"
        )

        print(
            f"Equação estimada:\n"
            f"y = "
            f"{self.coeficiente_angular:.2f}x + "
            f"{self.coeficiente_linear:.2f}"
        )

    # =====================================================
    # PREVISÃO
    # =====================================================

    def prever_geracao(
        self,
        passos_futuros: int = 5
    ) -> List[float]:
        """
        Prevê geração futura utilizando regressão.
        """

        print("\n[PREVISÃO DE GERAÇÃO]\n")

        previsoes = []

        ultimo_indice = len(self.vetor_tempo)

        for i in range(passos_futuros):

            x_futuro = ultimo_indice + i

            y_previsto = (
                self.coeficiente_angular * x_futuro
                + self.coeficiente_linear
            )

            previsoes.append(y_previsto)

            print(
                f"T+{i+1} -> "
                f"{y_previsto:.2f}"
            )

        return previsoes

    # =====================================================
    # SIMULAÇÕES
    # =====================================================

    def simular_cenarios(self):
        """
        Simula cenários operacionais.
        """

        print("\n[SIMULAÇÃO DE CENÁRIOS]\n")

        if len(self.vetor_geracao_solar) == 0:
            print("Sem dados disponíveis.")
            return

        media_solar = np.mean(
            self.vetor_geracao_solar
        )

        media_eolica = np.mean(
            self.vetor_geracao_eolica
        )

        media_consumo = np.mean(
            self.vetor_consumo
        )

        cenarios = {
            "NORMAL": {
                "solar": media_solar,
                "eolica": media_eolica,
                "consumo": media_consumo
            },

            "TEMPESTADE_DE_AREIA": {
                "solar": media_solar * 0.25,
                "eolica": media_eolica * 1.40,
                "consumo": media_consumo * 1.15
            },

            "FALHA_ENERGÉTICA": {
                "solar": media_solar * 0.40,
                "eolica": media_eolica * 0.50,
                "consumo": media_consumo * 1.30
            },

            "EXPANSÃO_DA_COLÔNIA": {
                "solar": media_solar * 1.50,
                "eolica": media_eolica * 1.60,
                "consumo": media_consumo * 1.80
            }
        }

        for nome, dados in cenarios.items():

            saldo = (
                dados["solar"]
                + dados["eolica"]
                - dados["consumo"]
            )

            print(
                f"{nome}\n"
                f" Solar: {dados['solar']:.2f}\n"
                f" Eólica: {dados['eolica']:.2f}\n"
                f" Consumo: {dados['consumo']:.2f}\n"
                f" Saldo Energético: {saldo:.2f}\n"
            )

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def exibir_estatisticas(self):

        print("\n[ESTATÍSTICAS GERAIS]\n")

        if len(self.vetor_geracao_solar) == 0:
            return

        print(
            f"Média Solar: "
            f"{np.mean(self.vetor_geracao_solar):.2f}"
        )

        print(
            f"Média Eólica: "
            f"{np.mean(self.vetor_geracao_eolica):.2f}"
        )

        print(
            f"Média Consumo: "
            f"{np.mean(self.vetor_consumo):.2f}"
        )

        print(
            f"Desvio Solar: "
            f"{np.std(self.vetor_geracao_solar):.2f}"
        )


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

engine = PredictionEngine()

# ==============================================
# HISTÓRICO
# ==============================================

engine.adicionar_registro(
    geracao_solar=500,
    geracao_eolica=220,
    consumo=600
)

engine.adicionar_registro(
    geracao_solar=540,
    geracao_eolica=230,
    consumo=640
)

engine.adicionar_registro(
    geracao_solar=610,
    geracao_eolica=240,
    consumo=700
)

engine.adicionar_registro(
    geracao_solar=680,
    geracao_eolica=260,
    consumo=740
)

engine.adicionar_registro(
    geracao_solar=720,
    geracao_eolica=300,
    consumo=790
)

# ==============================================
# REGRESSÃO
# ==============================================

engine.executar_regressao_linear()

# ==============================================
# PREVISÃO
# ==============================================

engine.prever_geracao(
    passos_futuros=5
)

# ==============================================
# SIMULAÇÕES
# ==============================================

engine.simular_cenarios()

# ==============================================
# ESTATÍSTICAS
# ==============================================

engine.exibir_estatisticas()