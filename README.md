# 🌊 SurfCast – Ocean & Weather Forecast Data Processing

Este projeto integra dados meteorológicos e marítimos da **Open-Meteo API** para apoiar previsões e análises relacionadas com o **surf**.  
Os dados são obtidos em formato JSON e processados para extrair informações diárias e horárias como:
- Altura e direção das ondas  
- Período das ondas e ondulação  
- Temperatura da superfície do mar  
- Índice UV máximo  
- Duração do dia (daylight duration)  
- Horas de nascer e pôr do sol  

---

## ⚙️ Fluxo de trabalho

1. **Recolha dos dados**
   - Os dados são obtidos através dé dois endpoints da Open-Meteo:
     ```
     https://marine-api.open-meteo.com/v1/marine
     ```
   - A resposta inclui variáveis horárias (ondas, temperatura, etc.) e diárias (nascer/pôr do sol, duração do dia, UV...).

2. **Conversão dos dados em KNIME**
   - O JSON gerado pela API é importado para o KNIME utilizando o nó **JSON Reader**.
   - São extraídos e normalizados os campos de interesse para posterior análise e visualização.

---

## 🕓 Conversão de `daylight_duration` de segundos para formato `HH:MM`

Os valores da duração do dia vêm da API em **segundos** (ex: `40491.45`) e são convertidos para o formato legível `HH:MM` (ex: `11:14`).

### 🧩 Implementação em KNIME
