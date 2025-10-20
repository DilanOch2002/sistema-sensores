// PRIMERO definir las constantes, LUEGO el console.log
const AUTH_SERVICE_URL = import.meta.env.VITE_API_BASE || 'http://localhost:5000';
const SENSORS_SERVICE_URL = 'http://localhost:5003';
const INGESTION_SERVICE_URL = 'http://localhost:5001';
const PLOTS_SERVICE_URL = 'http://localhost:5002';

// LUEGO el console.log
console.log('🔧 URLs de API:', {
  auth: AUTH_SERVICE_URL,
  sensors: SENSORS_SERVICE_URL, 
  plots: PLOTS_SERVICE_URL
});

// Servicio A - Autenticación CORREGIDO
export const authAPI = {
  login: async (email, password) => {
    console.log('🔐 Llamando a auth/login');
    try {
      const response = await fetch(`${AUTH_SERVICE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      console.log('📊 Respuesta auth:', response.status);
      return response.json();
    } catch (error) {
      console.error('❌ Error auth:', error);
      throw error;
    }
  },

  register: async (userData) => {
    const response = await fetch(`${AUTH_SERVICE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  },

  verify: async (token) => {
    const response = await fetch(`${AUTH_SERVICE_URL}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token })
    });
    return response.json();
  }
};

// Servicio B - Sensores CORREGIDO
export const sensorsAPI = {
  getLatest: async () => {
    console.log('📡 Llamando a sensors/latest');
    try {
      const response = await fetch(`${SENSORS_SERVICE_URL}/sensors/latest`);
      console.log('📊 Respuesta sensors:', response.status);
      const data = await response.json();
      console.log('✅ Datos sensors:', data);
      return data;
    } catch (error) {
      console.error('❌ Error sensors:', error);
      throw error;
    }
  },

  getHistorical: async (hours = 24) => {
    console.log('📈 Llamando a sensors/historical');
    try {
      const response = await fetch(`${SENSORS_SERVICE_URL}/sensors/historical?hours=${hours}`);
      return response.json();
    } catch (error) {
      console.error('❌ Error historical:', error);
      throw error;
    }
  }
};

// Servicio C - Ingesta CORREGIDO
export const ingestionAPI = {
  ingestData: async (sensorData) => {
    console.log('📨 Llamando a ingestion/ingest');
    try {
      const response = await fetch(`${INGESTION_SERVICE_URL}/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sensorData)
      });
      return response.json();
    } catch (error) {
      console.error('❌ Error ingestion:', error);
      throw error;
    }
  },

  batchIngest: async (sensorDataArray) => {
    const response = await fetch(`${INGESTION_SERVICE_URL}/batch-ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensorDataArray)
    });
    return response.json();
  },

  stressTest: async (config = {}) => {
    const response = await fetch(`${INGESTION_SERVICE_URL}/stress-test`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    return response.json();
  }
};

// Servicio D - Parcelas CORREGIDO
export const plotsAPI = {
  getAll: async () => {
    console.log('🌱 Llamando a plots/');
    try {
      const response = await fetch(`${PLOTS_SERVICE_URL}/plots`);
      console.log('📊 Respuesta plots:', response.status);
      const data = await response.json();
      console.log('✅ Datos plots:', data);
      return data;
    } catch (error) {
      console.error('❌ Error plots:', error);
      throw error;
    }
  },

  create: async (plotData) => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(plotData)
    });
    return response.json();
  },

  getById: async (plotId) => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots/${plotId}`);
    return response.json();
  },

  update: async (plotId, plotData) => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots/${plotId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(plotData)
    });
    return response.json();
  },

  delete: async (plotId, reason = 'Sin razón especificada') => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots/${plotId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason })
    });
    return response.json();
  },

  getDeleted: async () => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots/deleted`);
    return response.json();
  },

  getStats: async () => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots/stats`);
    return response.json();
  }
};

// Health checks
export const healthAPI = {
  checkAuth: async () => {
    const response = await fetch(`${AUTH_SERVICE_URL}/health`);
    return response.json();
  },

  checkSensors: async () => {
    const response = await fetch(`${SENSORS_SERVICE_URL}/health`);
    return response.json();
  },

  checkIngestion: async () => {
    const response = await fetch(`${INGESTION_SERVICE_URL}/health`);
    return response.json();
  },

  checkPlots: async () => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/health`);
    return response.json();
  }
};