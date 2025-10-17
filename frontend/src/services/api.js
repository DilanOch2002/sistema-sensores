// URLs de Render - REEMPLAZA con tus URLs reales después del deploy
const AUTH_SERVICE_URL = 'https://auth-service.onrender.com';
const SENSORS_SERVICE_URL = 'https://sensors-service.onrender.com';
const INGESTION_SERVICE_URL = 'https://ingestion-service.onrender.com';
const PLOTS_SERVICE_URL = 'https://plots-service.onrender.com';

// Servicio A - Autenticación
export const authAPI = {
  login: async (email, password) => {
    const response = await fetch(`${AUTH_SERVICE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    return response.json();
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

// Servicio B - Sensores
export const sensorsAPI = {
  getLatest: async () => {
    const response = await fetch(`${SENSORS_SERVICE_URL}/sensors/latest`);
    return response.json();
  },

  getHistorical: async (hours = 24) => {
    const response = await fetch(`${SENSORS_SERVICE_URL}/sensors/historical?hours=${hours}`);
    return response.json();
  }
};

// Servicio C - Ingesta
export const ingestionAPI = {
  ingestData: async (sensorData) => {
    const response = await fetch(`${INGESTION_SERVICE_URL}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensorData)
    });
    return response.json();
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

// Servicio D - Parcelas
export const plotsAPI = {
  getAll: async () => {
    const response = await fetch(`${PLOTS_SERVICE_URL}/plots`);
    return response.json();
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