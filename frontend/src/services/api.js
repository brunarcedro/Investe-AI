import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Health check
export const healthCheck = async () => {
  const response = await api.get('/');
  return response.data;
};

// Classificar perfil de risco
export const classificarPerfil = async (dados) => {
  const response = await api.post('/api/classificar-perfil', dados);
  return response.data;
};

// Recomendar portfolio (endpoint principal)
export const recomendarPortfolio = async (dados) => {
  const response = await api.post('/api/recomendar-portfolio', dados);
  return response.data;
};

// Informações do sistema
export const infoSistema = async () => {
  const response = await api.get('/api/info-sistema');
  return response.data;
};

// ============= SIMULAÇÃO (NOVO) =============

// Simular backtesting com dados reais
export const simularBacktesting = async (dados) => {
  const response = await api.post('/api/simular-backtesting', dados);
  return response.data;
};

// Comparar com benchmarks
export const compararBenchmarks = async (dados) => {
  const response = await api.post('/api/comparar-benchmarks', dados);
  return response.data;
};

// Projetar Monte Carlo
export const projetarMonteCarlo = async (dados) => {
  const response = await api.post('/api/projetar-monte-carlo', dados);
  return response.data;
};

// Cenários detalhados
export const cenariosDetalhados = async (dados) => {
  const response = await api.post('/api/cenarios-detalhados', dados);
  return response.data;
};

export default api;
