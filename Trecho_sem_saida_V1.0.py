""" 
# TRECHO SEM SAÍDA (Dead-end streets)

Juliana Lombard Souza

Identifica os trechos que configuram ruas sem saída e trechos isolados (trechos com nós de início ou fim de apenas grau 1)
"""

# ==============================================================================
# IDENTIFICAR RUAS SEM SAÍDA E TRECHOS ISOLADOS
# ==============================================================================
import geopandas as gpd
import networkx as nx
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DE CAMINHOS
# ==============================================================================
# Obtém o caminho absoluto da pasta onde o script está sendo executado
SCRIPT_DIR = Path(__file__).resolve().parent

# Define o caminho para a pasta raiz do projeto
PROJECT_ROOT = SCRIPT_DIR.parent

# Define os caminhos para as pastas de dados e de saída
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Cria a pasta de saída se ela não existir
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define os caminhos para os arquivos de entrada e saída
rede_shp = DATA_DIR / "rede_teste_lin.shp" # renomeie aqui
output_shp_path = OUTPUT_DIR / "rede_teste_ruas_sem_saida_lin.shp" # renomeie aqui
# ==============================================================================

def main():
    print("--- Iniciando a Análise de Ruas Sem Saída ---")

    # 1. Carregar o shapefile de arestas
    print(f"Carregando o arquivo de rede: {rede_shp}")
    try:
        gdf_edges = gpd.read_file(rede_shp)
    except Exception as e:
        raise FileNotFoundError(f"ERRO: Não foi possível ler o shapefile '{rede_shp}'. Verifique se o arquivo .shp e seus arquivos associados (.dbf, .shx) existem na pasta 'data'. Erro original: {e}")

    # 1.5. Limpeza Proativa dos Dados
    # Remove todas as linhas que possuem geometria nula ou vazia
    initial_count = len(gdf_edges)
    gdf_edges = gdf_edges[gdf_edges.geometry.notnull()]
    final_count = len(gdf_edges)
    if initial_count != final_count:
        print(f"Limpeza de dados: {initial_count - final_count} feições com geometria nula foram removidas.")
    print(f"Total de feições válidas para análise: {final_count}.")


    # 2. Construir o grafo com NetworkX
    print("\nConstruindo o grafo da rede...")
    G = nx.Graph()
    
    # Adiciona as arestas ao grafo a partir das geometrias
    for _, line in gdf_edges.iterrows():
            if line.geometry is not None and not line.geometry.is_empty:
                start_point = line.geometry.coords[0]
                end_point = line.geometry.coords[-1]
                G.add_edge(start_point, end_point)

    # 3. Identificar nós de grau 1 (pontas de rua sem saída)
    print("Identificando nós de grau 1...")
    degree_1_nodes = [node for node, degree in G.degree() if degree == 1]
    print(f"Encontrados {len(degree_1_nodes)} nós de grau 1.")

    # 4. Filtrar as arestas conectadas a esses nós
    print("Filtrando os trechos de rua sem saída...")
    dead_end_edges = []
    
    # Conjunto para verificação rápida
    degree_1_nodes_set = set(degree_1_nodes)

    for _, edge in gdf_edges.iterrows():
        start_point = edge.geometry.coords[0]
        end_point = edge.geometry.coords[-1]
        
        # Se o início OU o fim do trecho for um nó de grau 1, é uma rua sem saída
        if start_point in degree_1_nodes_set or end_point in degree_1_nodes_set:
            dead_end_edges.append(edge)

    # Criar um novo GeoDataFrame com os resultados
    gdf_dead_ends = gpd.GeoDataFrame(dead_end_edges, crs=gdf_edges.crs)

    print(f"Identificados {len(gdf_dead_ends)} trechos de ruas sem saída.")

    # 5. Salvar o resultado em um novo shapefile
    print(f"Salvando o resultado em: {output_shp_path}")
    gdf_dead_ends.to_file(output_shp_path)
    
    print("\n--- Análise concluída com sucesso! ---")


if __name__ == "__main__":
    main()