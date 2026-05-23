from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import numpy as np


# =========================================================
# MODELO
# =========================================================

@dataclass
class RegistroProcessado:
    sensor_id: str
    tipo: str
    valor: float
    timestamp: datetime


# =========================================================
# PROCESSING ENGINE
# =========================================================

class ProcessingEngine:
    """
    Camada responsável pelo processamento dos dados
    da colônia Aurora.

    Responsabilidades:
    - limpeza de dados;
    - validação;
    - cálculos;
    - estatísticas;
    - agregações;
    - atualização de estados.
    """

    def __init__(self):

        # ==============================================
        # Histórico processado
        # ==============================================
        self.dados_processados: List[RegistroProcessado] = []

        # ==============================================
        # Vetores NumPy
        # ==============================================
        self.vetor_temperaturas = np.array([])
        self.vetor_consumo = np.array([])

        # ==============================================
        # Matrizes NumPy
        # Linhas -> módulos
        # Colunas -> tempo
        # ==============================================
        self.matriz_operacional = np.zeros((5, 24))

        # ==============================================
        # Estatísticas
        # ==============================================
        self.estatisticas: Dict[str, Dict] = {}

        # ==============================================
        # Estados do sistema
        # ==============================================
        self.estado_colonia = {
            "energia": "ESTÁVEL",
            "temperatura": "NORMAL",
            "estrutura": "SEGURA"
        }

    # =====================================================
    # LIMPEZA E VALIDAÇÃO
    # =====================================================

    def limpar_dados(
        self,
        registros: List[RegistroProcessado]
    ) -> List[RegistroProcessado]:
        """
        Remove registros inválidos.
        """

        dados_limpos = []

        for registro in registros:

            if registro.valor is None:
                continue

            if np.isnan(registro.valor):
                continue

            dados_limpos.append(registro)

        print(
            f"[LIMPEZA] "
            f"{len(dados_limpos)} registros válidos."
        )

        return dados_limpos

    def validar_dados(
        self,
        registro: RegistroProcessado
    ) -> bool:
        """
        Realiza validação operacional.
        """

        limites = {
            "temperatura_interna": (-20, 50),
            "temperatura_externa": (-150, 80),
            "velocidade_vento": (0, 250),
            "geracao_solar": (0, 1500),
            "geracao_eolica": (0, 1200),
            "consumo_energetico": (0, 5000),
            "integridade_estrutural": (0, 100)
        }

        if registro.tipo not in limites:
            return False

        minimo, maximo = limites[registro.tipo]

        valido = minimo <= registro.valor <= maximo

        print(
            f"[VALIDAÇÃO] "
            f"{registro.sensor_id} -> {valido}"
        )

        return valido

    # =====================================================
    # MÉDIA
    # =====================================================

    def calcular_media(
        self,
        vetor: np.ndarray
    ) -> float:
        """
        Calcula média vetorizada.
        """

        if len(vetor) == 0:
            return 0

        media = float(np.mean(vetor))

        print(f"[MÉDIA] {media:.2f}")

        return media

    # =====================================================
    # MATRIZ
    # =====================================================

    def atualizar_matriz(
        self,
        modulo: int,
        horario: int,
        valor: float
    ):
        """
        Atualiza matriz operacional.
        """

        self.matriz_operacional[modulo][horario] = valor

        print(
            f"[MATRIZ] "
            f"Módulo {modulo} "
            f"Hora {horario} "
            f"Valor {valor}"
        )

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================

    def processar_estatisticas(self):
        """
        Calcula estatísticas globais.
        """

        print("\n[PROCESSAMENTO ESTATÍSTICO]\n")

        if len(self.vetor_temperaturas) > 0:

            self.estatisticas["temperaturas"] = {
                "media": float(
                    np.mean(self.vetor_temperaturas)
                ),
                "maximo": float(
                    np.max(self.vetor_temperaturas)
                ),
                "minimo": float(
                    np.min(self.vetor_temperaturas)
                ),
                "desvio_padrao": float(
                    np.std(self.vetor_temperaturas)
                )
            }

        if len(self.vetor_consumo) > 0:

            self.estatisticas["consumo"] = {
                "media": float(
                    np.mean(self.vetor_consumo)
                ),
                "pico": float(
                    np.max(self.vetor_consumo)
                ),
                "minimo": float(
                    np.min(self.vetor_consumo)
                )
            }

        for categoria, valores in self.estatisticas.items():

            print(f"{categoria.upper()}")

            for chave, valor in valores.items():
                print(f" - {chave}: {valor:.2f}")

    # =====================================================
    # AGREGAÇÕES
    # =====================================================

    def executar_agregacoes(
        self,
        registros: List[RegistroProcessado]
    ):
        """
        Executa agrupamentos e agregações.
        """

        print("\n[AGREGAÇÕES]\n")

        agregacoes = {}

        for registro in registros:

            if registro.tipo not in agregacoes:
                agregacoes[registro.tipo] = []

            agregacoes[registro.tipo].append(
                registro.valor
            )

        for tipo, valores in agregacoes.items():

            media = np.mean(valores)
            soma = np.sum(valores)

            print(
                f"{tipo}\n"
                f" -> média: {media:.2f}\n"
                f" -> soma: {soma:.2f}\n"
            )

    # =====================================================
    # ESTADOS
    # =====================================================

    def atualizar_estados(self):
        """
        Atualiza estados globais da colônia.
        """

        print("\n[ATUALIZAÇÃO DE ESTADOS]\n")

        media_temp = self.calcular_media(
            self.vetor_temperaturas
        )

        media_consumo = self.calcular_media(
            self.vetor_consumo
        )

        # ==========================================
        # TEMPERATURA
        # ==========================================

        if media_temp > 35:
            self.estado_colonia["temperatura"] = "CRÍTICA"

        elif media_temp > 28:
            self.estado_colonia["temperatura"] = "ALERTA"

        else:
            self.estado_colonia["temperatura"] = "NORMAL"

        # ==========================================
        # ENERGIA
        # ==========================================

        if media_consumo > 3000:
            self.estado_colonia["energia"] = "SOBRECARGA"

        elif media_consumo > 1800:
            self.estado_colonia["energia"] = "ALERTA"

        else:
            self.estado_colonia["energia"] = "ESTÁVEL"

        for chave, valor in self.estado_colonia.items():

            print(f"{chave.upper()} -> {valor}")

    # =====================================================
    # INGESTÃO
    # =====================================================

    def adicionar_registro(
        self,
        sensor_id: str,
        tipo: str,
        valor: float
    ):

        registro = RegistroProcessado(
            sensor_id=sensor_id,
            tipo=tipo,
            valor=valor,
            timestamp=datetime.now()
        )

        if not self.validar_dados(registro):
            print("[DESCARTADO]")
            return

        self.dados_processados.append(registro)

        # ==========================================
        # Vetores especializados
        # ==========================================

        if "temperatura" in tipo:

            self.vetor_temperaturas = np.append(
                self.vetor_temperaturas,
                valor
            )

        if "consumo" in tipo:

            self.vetor_consumo = np.append(
                self.vetor_consumo,
                valor
            )

        print(
            f"[PROCESSADO] "
            f"{sensor_id} -> {valor}"
        )


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

engine = ProcessingEngine()

# ==============================================
# REGISTROS
# ==============================================

engine.adicionar_registro(
    "TEMP-INT-01",
    "temperatura_interna",
    24.8
)

engine.adicionar_registro(
    "TEMP-INT-02",
    "temperatura_interna",
    29.3
)

engine.adicionar_registro(
    "ENERGIA-01",
    "consumo_energetico",
    2100
)

engine.adicionar_registro(
    "ENERGIA-02",
    "consumo_energetico",
    3200
)

# ==============================================
# MÉDIA
# ==============================================

engine.calcular_media(
    engine.vetor_temperaturas
)

# ==============================================
# MATRIZ
# ==============================================

engine.atualizar_matriz(
    modulo=1,
    horario=14,
    valor=88.7
)

# ==============================================
# ESTATÍSTICAS
# ==============================================

engine.processar_estatisticas()

# ==============================================
# AGREGAÇÕES
# ==============================================

engine.executar_agregacoes(
    engine.dados_processados
)

# ==============================================
# ESTADOS
# ==============================================

engine.atualizar_estados()