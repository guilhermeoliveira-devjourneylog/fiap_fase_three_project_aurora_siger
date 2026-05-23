from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import numpy as np


# =========================================================
# MODELOS
# =========================================================

@dataclass
class Telemetria:
    sensor_id: str
    tipo: str
    valor: float
    timestamp: datetime


# =========================================================
# NÓ DA ÁRVORE HIERÁRQUICA
# =========================================================

class TreeNode:

    def __init__(self, nome: str):

        self.nome = nome
        self.filhos: List["TreeNode"] = []

    def adicionar_filho(self, node: "TreeNode"):

        self.filhos.append(node)

    def exibir(self, nivel=0):

        print("   " * nivel + f"- {self.nome}")

        for filho in self.filhos:
            filho.exibir(nivel + 1)


# =========================================================
# STORAGE MANAGER
# =========================================================

class StorageManager:
    """
    Camada responsável pelo armazenamento e organização
    das informações da colônia Aurora.

    Estruturas utilizadas:
    - listas;
    - vetores;
    - matrizes;
    - tabelas hash;
    - árvores hierárquicas.
    """

    def __init__(self):

        # ==============================================
        # LISTAS
        # Histórico linear de telemetria
        # ==============================================
        self.historico: List[Telemetria] = []

        # ==============================================
        # VETORES
        # Vetores NumPy para cálculos rápidos
        # ==============================================
        self.buffer_temperaturas = np.array([])

        # ==============================================
        # MATRIZES
        # Matriz de consumo energético
        # Linhas = módulos
        # Colunas = intervalos temporais
        # ==============================================
        self.matriz_energia = np.zeros((5, 24))

        # ==============================================
        # HASH TABLE
        # Indexação rápida por sensor_id
        # ==============================================
        self.hash_telemetria: Dict[str, List[Telemetria]] = {}

        # ==============================================
        # ÁRVORE HIERÁRQUICA
        # Organização estrutural da colônia
        # ==============================================
        self.arvore_colonia = TreeNode("Aurora")

        self._inicializar_arvore()

    # =====================================================
    # INICIALIZAÇÃO DA ÁRVORE
    # =====================================================

    def _inicializar_arvore(self):

        energia = TreeNode("Energia")
        sensores = TreeNode("Sensores")
        infraestrutura = TreeNode("Infraestrutura")

        energia.adicionar_filho(TreeNode("Solar"))
        energia.adicionar_filho(TreeNode("Eólica"))
        energia.adicionar_filho(TreeNode("Consumo"))

        sensores.adicionar_filho(TreeNode("Temperatura"))
        sensores.adicionar_filho(TreeNode("Vento"))

        infraestrutura.adicionar_filho(TreeNode("Módulos"))
        infraestrutura.adicionar_filho(TreeNode("Integridade"))

        self.arvore_colonia.adicionar_filho(energia)
        self.arvore_colonia.adicionar_filho(sensores)
        self.arvore_colonia.adicionar_filho(infraestrutura)

    # =====================================================
    # ARMAZENAMENTO
    # =====================================================

    def armazenar_telemetria(
        self,
        sensor_id: str,
        tipo: str,
        valor: float
    ):

        registro = Telemetria(
            sensor_id=sensor_id,
            tipo=tipo,
            valor=valor,
            timestamp=datetime.now()
        )

        # ==========================================
        # LISTA
        # ==========================================
        self.historico.append(registro)

        # ==========================================
        # HASH TABLE
        # ==========================================
        if sensor_id not in self.hash_telemetria:
            self.hash_telemetria[sensor_id] = []

        self.hash_telemetria[sensor_id].append(registro)

        # ==========================================
        # VETOR
        # ==========================================
        if "temperatura" in tipo.lower():

            self.buffer_temperaturas = np.append(
                self.buffer_temperaturas,
                valor
            )

        print(
            f"[ARMAZENADO] "
            f"{sensor_id} -> {valor}"
        )

    # =====================================================
    # CONSULTA
    # =====================================================

    def consultar_historico(
        self,
        sensor_id: Optional[str] = None
    ) -> List[Telemetria]:

        if sensor_id:

            print(
                f"\n[CONSULTA HASH] "
                f"{sensor_id}"
            )

            return self.hash_telemetria.get(
                sensor_id,
                []
            )

        print("\n[CONSULTA GLOBAL]")

        return self.historico

    # =====================================================
    # HASH
    # =====================================================

    def atualizar_hash(self):

        print("\n[ATUALIZAÇÃO HASH]\n")

        for sensor_id, registros in self.hash_telemetria.items():

            conteudo = "".join(
                f"{r.valor}{r.timestamp}"
                for r in registros
            )

            hash_integridade = hashlib.sha256(
                conteudo.encode()
            ).hexdigest()

            print(
                f"Sensor: {sensor_id}\n"
                f"Hash: {hash_integridade}\n"
            )

    # =====================================================
    # MATRIZ ENERGÉTICA
    # =====================================================

    def atualizar_matriz_energia(
        self,
        modulo: int,
        hora: int,
        consumo: float
    ):

        self.matriz_energia[modulo][hora] = consumo

    def exibir_matriz_energia(self):

        print("\n[MATRIZ ENERGÉTICA]\n")

        print(self.matriz_energia)

    # =====================================================
    # VETORES
    # =====================================================

    def calcular_media_temperaturas(self):

        if len(self.buffer_temperaturas) == 0:
            return 0

        media = np.mean(self.buffer_temperaturas)

        print(
            f"\n[MÉDIA TEMPERATURAS] "
            f"{media:.2f}"
        )

        return media

    # =====================================================
    # ÁRVORE
    # =====================================================

    def exibir_hierarquia(self):

        print("\n[ÁRVORE HIERÁRQUICA]\n")

        self.arvore_colonia.exibir()


# =========================================================
# EXEMPLO DE UTILIZAÇÃO
# =========================================================

storage = StorageManager()

# ==============================================
# ARMAZENAMENTO
# ==============================================

storage.armazenar_telemetria(
    "TEMP-INT-01",
    "temperatura_interna",
    24.5
)

storage.armazenar_telemetria(
    "VENTO-01",
    "velocidade_vento",
    83.2
)

storage.armazenar_telemetria(
    "SOLAR-01",
    "geracao_solar",
    720.8
)

# ==============================================
# CONSULTA
# ==============================================

dados = storage.consultar_historico(
    "TEMP-INT-01"
)

for item in dados:
    print(item)

# ==============================================
# HASH
# ==============================================

storage.atualizar_hash()

# ==============================================
# MATRIZ
# ==============================================

storage.atualizar_matriz_energia(
    modulo=0,
    hora=10,
    consumo=520
)

storage.exibir_matriz_energia()

# ==============================================
# VETORES
# ==============================================

storage.calcular_media_temperaturas()

# ==============================================
# ÁRVORE
# ==============================================

storage.exibir_hierarquia()