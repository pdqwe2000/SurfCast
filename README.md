# 🌊 SurfCast – Ocean & Weather Forecast Data Processing

Integração de Sistemas de Informação

Licenciatura em Engenharia de Sistemas Informáticos (*regime pós-laboral*) 2025-26


| Número | Nome |
| -----   | ---- |
| 27990     | Pedro Duarte  |

## Organização

[surf_data/](./surf_data/)  dados recebidos da API após ser processados pelo Python

[Workflows/](./Workflows/)  Workflows para tratamento de dados, conexões à API 

## Introdução
Este projeto integra dados meteorológicos e marítimos da **Open-Meteo API** para apoiar previsões e análises relacionadas com o **surf**.  

## Objetivo
Este projeto visa desenvolver uma solução para manipular dados metereológicos, utilizando  API's. Os dados são obtidos em e processados para extrair informações diárias e horárias como:
- Altura e direção das ondas  
- Período das ondas e ondulação  
- Temperatura da superfície do mar  
- Índice UV máximo  
- Duração do dia (daylight duration)  
- Horas de nascer e pôr do sol  

---

## ⚙️ Fluxo de trabalho

1. **Recolha dos dados**
    - Os dados são obtidos através de dois endpoints da Open-Meteo:

    - O endpoint abaixo conecta á api maritima e tráz variáveis Marítimas (ondas, direção, swell, etc.) e diárias (Onda máxima e Direção Dominante).  
     ```
     https://marine-api.open-meteo.com/v1/marine
     ```
    
    - O endpoint abaixo conecta á api de forecast e tráz variáveis horárias (temperatura, vento, percipitação etc.) e diárias (nascer/pôr do sol, duração do dia, UV).
     ```
     https://marine-api.open-meteo.com/v1/forecast
     ```

2. **Conversão dos dados em KNIME**
    - O JSON gerado pela API é importado para o KNIME utilizando o nó **JSON Reader**.
    - São extraídos e normalizados os campos de interesse para posterior análise e visualização.
3. **Conexão de dados no KNIME**
    - Uma conexção à API é usado através do nó **Get Request**.
    - São extraídos e normalizados os campos de interesse para posterior análise e visualização.
---

## 🕓 Conversão de `daylight_duration` de segundos para formato `HH:MM`

Os valores da duração do dia vêm da API em **segundos** (ex: `40491.45`) e são convertidos para o formato legível `HH:MM` (ex: `11:14`).

### 🧩 Implementação em KNIME
