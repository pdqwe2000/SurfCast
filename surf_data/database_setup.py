import sqlite3

# Cria (ou liga-se a) uma base de dados local
conn = sqlite3.connect("surfcast.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude TEXT,
    longitude TEXT
)
""")



# Cria tabela para previsões diárias
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    times TEXT,
    sunrises TEXT,
    sunsets TEXT,
    uv_index_maxs REAL,
    daylight_durations TEXT,
    latitude REAL,
    longitude REAL,
    wave_height_maxs REAL,
    wave_direction_dominants INTEGER,
    classification TEXT
)
""")

# Cria tabela para previsões horárias
#  cursor.execute("""
# CREATE TABLE IF NOT EXISTS hourly_forecast (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     dates TEXT,
#     wave_heights REAL,
#     wave_directions REAL,
#     wave_periods REAL,
#     swell_wave_heights REAL,
#     swell_wave_directions REAL,
#     swell_wave_periods REAL,
#     wind_wave_heights REAL,
#     wind_wave_directions REAL,
#     wind_wave_periods REAL,
#     sea_surface_temperatures REAL
# """)

conn.commit()
conn.close()

print("✅ Base de dados e tabelas criadas com sucesso!")