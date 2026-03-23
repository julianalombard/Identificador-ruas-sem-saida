# Identificador de Ruas Sem Saída (Dead-End Streets)

**Juliana Lombard Souza**

Este algoritmo identifica ruas sem saída em uma rede de linhas (como uma rede viária). Ele analisa a topologia da rede para encontrar todos os segmentos de linha que terminam em um "beco" sem continuidade, gerando um novo shapefile contendo apenas esses trechos específicos.

## Funcionalidades

*   Carrega uma rede de um arquivo shapefile de linhas.
*   Realiza a limpeza de dados, removendo geometrias nulas ou vazias.
*   Constrói um modelo de grafo da rede usando a biblioteca `networkx`.
*   Identifica nós de grau 1 (pontos finais de ruas sem saída).
*   Filtra e extrai todos os trechos de linha conectados a esses nós.
*   Salva o resultado em um novo shapefile na pasta `output`, contendo apenas as ruas sem saída.

## Pré-requisitos

Antes de executar o script, certifique-se de ter o Python 3.x e as seguintes bibliotecas instaladas. Você pode instalá-las usando o `pip`:

```bash
pip install geopandas networkx
```

> **Nota:** A biblioteca `pathlib` já vem incluída na instalação padrão do Python.

## Como Usar

Siga os passos abaixo para configurar e executar o script em sua máquina.

### 1. Estrutura do Projeto

Organize seus arquivos da seguinte forma. O script espera encontrar o arquivo de dados na pasta `data` e criará a pasta `output` automaticamente, se ela não existir.

```
meu_projeto_rede/
├── data/
│   └── rede_teste_lin.shp  # <-- Coloque seu arquivo shapefile aqui
├── output/
│   └── (será criada automaticamente pelo script)
└── scripts/
    └── ruas_sem_saida.py  # <-- O seu script Python
```

### 2. Preparar os Dados

1.  Coloque seu arquivo shapefile da rede (ex: `rede_teste_lin.shp`) e todos os arquivos associados (`.shx`, `.dbf`, etc.) dentro da pasta `data`.
2.  Verifique se o nome do arquivo no script corresponde ao seu arquivo. A linha a ser alterada está no início do script:

    ```python
    # Define os caminhos para os arquivos de entrada e saída
    rede_shp = DATA_DIR / "rede_teste_lin.shp" # renomeie aqui
    ```

### 3. Executar o Script

Abra o terminal ou prompt de comando, navegue até a pasta `scripts` e execute o script com o seguinte comando:

```bash
python ruas_sem_saida.py
```

### 4. Verificar os Resultados

Após a execução, verifique a pasta `output`. Você encontrará:

*   `rede_teste_ruas_sem_saida_lin.shp`: Um novo shapefile que contém apenas os trechos de linha que foram identificados como ruas sem saída. Você pode carregar este arquivo em um SIG (como QGIS) para visualizá-los sobre a rede original.

---

## 🔬 O que é uma Rua Sem Saída na Análise de Redes?

Neste contexto, uma "rua sem saída" (ou dead-end street) é um trecho que tem uma de suas extremidades desconectada do restante da rede principal.

Tecnicamente, isso acontece quando um trecho de linha (uma "aresta" no grafo) está conectado a um "nó" de **grau 1**.

*   **O que é o "grau" de um nó?** O grau de um nó é o número de arestas (ruas) conectadas a ele.
*   **O que é um nó de grau 1?** É um ponto final, uma "ponta" que não se conecta a nenhuma outra rua naquele ponto específico.

Esta análise é útil para:

*   Planejamento urbano e logística.
*   Identificar erros de digitalização em redes de infraestrutura.
*   Análises de acessibilidade e conectividade.

## Licença/Citação

MIT License 

Citation: SOUZA, J.L. (2026) Identificador de Ruas Sem Saída (Dead-End Streets) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19133887
