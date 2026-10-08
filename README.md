
# Crônicas do Espaço — Parte 1

Sistema de consulta e planejamento de missões com dados reais do Sistema Solar.
Estrutura implementada: **Tabela Hash** (encadeamento). Guloso: **Opção A** (triagem de missões).

**Executar:** `pip install requests python-dotenv` e `python main.py`
(opcional: copie `.env.example` para `.env` e coloque o token em `SOLAR_API_KEY`).

## 1. Fonte de dados

- **API:** The Solar System OpenData — https://api.le-systeme-solaire.net
- **Justificativa:** dados reais, JSON, ~550 corpos (planetas, luas, asteroides, cometas) com atributos físicos e orbitais suficientes para busca, filtro e otimização.
- **Endpoint:** `GET /rest/bodies` (cabeçalho `Authorization: Bearer <token>`)
- **Exemplo:** `GET https://api.le-systeme-solaire.net/rest/bodies`
- **Estrutura retornada:** `{"bodies": [ {...}, ... ]}`. Campos usados de cada corpo: `id`, `englishName`, `bodyType`, `isPlanet`, `mass{massValue,massExponent}`, `gravity`, `meanRadius`, `semimajorAxis`, `aroundPlanet{planet}`, `avgTemp`, `moons[]`.
- **Data da consulta:** 08/10/2026 (salva em `aquisicao/bodies.json`).
- **Módulo de aquisição (`aquisicao/api_solar.py`):** faz o GET em tempo de execução (Nível 1), grava o JSON localmente e, se a API falhar, usa o `bodies.json` local como contingência. Os dados são mapeados para objetos `CorpoCeleste` e guardados na tabela hash.

## 2. Modelagem

- **`CorpoCeleste`** (`modelos/corpoceleste.py`): id, nome, tipo, eh_planeta, massa (kg), gravidade (m/s²), raio (km), dist_orbital (km), ao_redor_de, temp_media (K), num_luas. `from_api` converte o JSON (ex.: massa = valor × 10^expoente).
- **Chave da hash:** nome em inglês, minúsculo.
- **Operações do menu (`main.py`):**

  1. *Consultar* corpo pelo nome exato (busca na hash, O(1) esperado);
  2. *Pesquisar* por trecho do nome;
  3. *Listar/filtrar* por tipo e gravidade mínima;
  4. *Planejar missão* (guloso);
  5. *Métricas* da hash (colisões, load factor, rehashes).
  6. *Comparar dois corpos* (operação adicional, tópico 6.4): exibe lado a lado
     tipo, massa, gravidade, raio, distância orbital, temperatura e número de luas
     de dois corpos. Justificativa: ao planejar uma missão, é preciso contrastar
     candidatos (ex.: Mars vs. Moon) antes de decidir o destino. Usa duas buscas
     na tabela hash, O(1) esperado cada.
- **Decisão:** pesquisa por trecho e filtros percorrem a hash inteira (`valores()`), O(n). Buscas por prefixo eficientes ficam para a Trie e consultas por faixa (ex.: distância) para a Árvore B, na Parte 2 (interfaces em `estruturas/interfaces.py`).

## 3. Estrutura de dados: Tabela Hash

- **Implementação própria** (`estruturas/tabela_hash.py`): vetor de buckets com listas encadeadas, função hash polinomial (base 31), tamanho inicial 16, dobra de tamanho (*rehash*) quando o fator de carga chega a 0,75. Nenhum `dict` é usado.
- **Justificativa:** o uso principal é localizar um corpo pelo nome, e a hash dá O(1) esperado para isso, sem precisar de ordenação.
- **Operações:** `inserir` (atualiza se a chave existe), `buscar`, `remover`, `_rehash`, `load_factor`, `valores`.
- **Complexidade:** inserir/buscar/remover O(1) esperado e O(n) no pior caso (todas as chaves no mesmo bucket); inserir com rehash O(n) pontual, mas O(1) amortizado (seção 4).
- **Instrumentação (impressa no terminal ao iniciar e na opção 5):** contador de colisões (inserção em bucket já ocupado, inclusive durante rehash), número de rehashes, tamanho e fator de carga atual. Resultado com a base atual: 554 corpos, tamanho 1024, 6 rehashes, 355 colisões, load factor 0,541.
- **Interfaces das demais estruturas:** `TrieInterface` (inserir, buscar, buscar_prefixo, remover, nos_visitados) e `ArvoreBInterface` (inserir, buscar, buscar_faixa, remover, total_splits, altura), em `estruturas/interfaces.py`. O sistema depende só desses contratos.

## 4. Análise amortizada: rehash

**Pior caso:** um único `inserir` que dispara o rehash move todos os ~0,75·T elementos para a nova tabela: O(n). Tratar *toda* inserção como O(n) é muito pessimista.

**Análise agregada.** O rehash ocorre quando n = 0,75·T e o tamanho passa a 2T. Começando em T = 16, os rehashes ocorrem nos tamanhos 16, 32, 64, ..., T_f, movendo 0,75·T elementos cada. O custo total de rehash nas n inserções é:

0,75·(16 + 32 + ... + T_f) < 0,75 · 2·T_f = 1,5·T_f = 2·n_f ≤ 2n,

pois a soma geométrica é menor que 2·T_f e n_f = 0,75·T_f é o número de elementos no último rehash. Somando as n inserções simples (custo O(1) esperado cada), o custo total é ≤ n + 2n = 3n, ou seja, **O(1) amortizado por inserção**.

**Método contábil.** Cobrar 3 moedas por inserção: 1 paga a própria inserção e 2 ficam guardadas. Após um rehash para tamanho T a carga é 0,375, então ocorrem 0,375·T inserções até o próximo rehash, acumulando 2 · 0,375·T = 0,75·T moedas, exatamente o custo de mover os 0,75·T elementos no próximo rehash. O saldo nunca fica negativo, logo o custo amortizado é 3 = O(1).

**Conferência experimental:** nas 554 inserções houve 6 rehashes, movendo 12+24+48+96+192+384 = 756 elementos, que é ≤ 2·554 = 1108, como previsto.

## 5. Algoritmo guloso: Opção A (triagem de missões)

- **Problema:** escolher destinos para visitar com um **orçamento limitado de distância total** (km), maximizando o potencial científico somado.
- **Candidato:** corpo com `dist_orbital` (custo) e `potencial = num_luas + 1 (se planeta anão) + 0,1·gravidade` (benefício).
- **Estratégia:** ordenar por razão benefício/custo (potencial ÷ distância) decrescente e escolher cada candidato enquanto couber no orçamento restante. Custo O(n log n).
- **Justificativa do critério:** a razão prioriza o que rende mais ciência por km gasto, e é a heurística clássica para a mochila (*knapsack*).
- **Resultado:** a lista de destinos escolhidos, o custo total e a sobra do orçamento são impressos na opção 4.
- **Limitações:** o problema é uma mochila 0/1, e o guloso por razão **não garante o ótimo**. Exemplo: orçamento 10, itens A (custo 6, benefício 7), B (custo 5, benefício 5), C (custo 5, benefício 5): o guloso escolhe A (razão 1,17) e sobram 4, que não cabem em B nem C, total 7; o ótimo é B+C, total 10. Além disso, o potencial é uma métrica simplificada (e a `dist_orbital` de luas é a distância até o planeta, não até a Terra), então os resultados são indicativos.
