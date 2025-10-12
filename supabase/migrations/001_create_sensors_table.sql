CREATE TABLE IF NOT EXISTS sensors (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(100) NOT NULL,
    temperature DECIMAL,
    humidity DECIMAL,
    timestamp TIMESTAMPTZ,
    latitude DECIMAL,
    longitude DECIMAL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_sensor_id ON sensors(sensor_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON sensors(timestamp);