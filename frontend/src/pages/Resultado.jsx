import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip as RechartsTooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, LineChart, Line } from 'recharts';
import { cenariosDetalhados, compararBenchmarks } from '../services/api';

export default function Resultado() {
  const navigate = useNavigate();
  const [resultado, setResultado] = useState(null);
  const [cenarios, setCenarios] = useState(null);
  const [loadingCenarios, setLoadingCenarios] = useState(false);
  const [benchmarks, setBenchmarks] = useState(null);
  const [loadingBenchmarks, setLoadingBenchmarks] = useState(false);

  useEffect(() => {
    const data = localStorage.getItem('resultado_investimento');
    if (data) {
      const parsedData = JSON.parse(data);
      setResultado(parsedData);

      // Buscar cenários detalhados se houver alocação
      if (parsedData.alocacao_recomendada) {
        fetchCenarios(parsedData);
        fetchBenchmarks(parsedData);
      }
    } else {
      navigate('/questionario');
    }
  }, [navigate]);

  const fetchBenchmarks = async (resultado) => {
    setLoadingBenchmarks(true);
    try {
      const alocacaoDecimal = {};
      Object.entries(resultado.alocacao_recomendada).forEach(([key, value]) => {
        const keyMap = {
          'Renda Fixa': 'renda_fixa',
          'Ações Brasil': 'acoes_brasil',
          'Ações Internacional': 'acoes_internacional',
          'Fundos Imobiliários': 'fundos_imobiliarios',
          'Commodities': 'commodities',
          'Criptomoedas': 'criptomoedas'
        };
        alocacaoDecimal[keyMap[key] || key] = parseFloat(value);
      });

      const response = await compararBenchmarks({
        alocacao: alocacaoDecimal,
        valor_inicial: 10000,
        aporte_mensal: 500,
        periodo: '5y'
      });

      setBenchmarks(response);
    } catch (error) {
      console.error('Erro ao buscar benchmarks:', error);
    } finally {
      setLoadingBenchmarks(false);
    }
  };

  const fetchCenarios = async (resultado) => {
    setLoadingCenarios(true);
    try {
      const alocacaoDecimal = {};
      Object.entries(resultado.alocacao_recomendada).forEach(([key, value]) => {
        // Convert back to English keys
        const keyMap = {
          'Renda Fixa': 'renda_fixa',
          'Ações Brasil': 'acoes_brasil',
          'Ações Internacional': 'acoes_internacional',
          'Fundos Imobiliários': 'fundos_imobiliarios',
          'Commodities': 'commodities',
          'Criptomoedas': 'criptomoedas'
        };
        alocacaoDecimal[keyMap[key] || key] = parseFloat(value);
      });

      const response = await cenariosDetalhados({
        alocacao: alocacaoDecimal,
        valor_inicial: 10000,
        aporte_mensal: 500,
        anos: resultado.metricas?.horizonte_anos || 10
      });

      setCenarios(response);
    } catch (error) {
      console.error('Erro ao buscar cenários:', error);
    } finally {
      setLoadingCenarios(false);
    }
  };

  if (!resultado) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-academic-bg">
        <div className="text-center">
          <div className="text-4xl mb-4">📊</div>
          <p className="text-lg text-academic-text font-semibold">Carregando resultados...</p>
        </div>
      </div>
    );
  }

  const chartData = Object.entries(resultado.alocacao_recomendada || {}).map(
    ([nome, valor]) => ({
      name: nome,
      value: parseFloat(valor),
      displayValue: `${valor}%`,
    })
  );

  const COLORS = ['#1E40AF', '#3B82F6', '#60A5FA', '#93BBFD', '#0EA5E9', '#38BDF8'];

  const getPerfilIcon = (perfil) => {
    if (perfil.includes('Conservador')) return '🛡️';
    if (perfil.includes('Moderado')) return '⚖️';
    if (perfil.includes('Arrojado')) return '🚀';
    return '📊';
  };

  const handleNovaAnalise = () => {
    localStorage.removeItem('resultado_investimento');
    localStorage.removeItem('perfil_investidor');
    localStorage.removeItem('dados_formulario');
    navigate('/questionario');
  };

  return (
    <div className="min-h-screen bg-academic-bg">
      {/* Header */}
      <header className="border-b border-academic-border bg-white sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2">
              <span className="text-xl font-bold text-primary">Investe-AI</span>
            </Link>
            <nav className="flex gap-4">
              <button onClick={handleNovaAnalise} className="text-sm text-academic-text-secondary hover:text-primary transition-colors font-medium">
                Nova Análise
              </button>
              <Link to="/" className="text-sm text-academic-text-secondary hover:text-primary transition-colors font-medium">
                Início
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Page Title */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-academic-text mb-2">
            Análise de Perfil Concluída
          </h1>
          <p className="text-academic-text-secondary">
            Resultado gerado por Arquitetura Dual de Redes Neurais Ensemble (Voting Classifier + Ensemble V4 Ultimate)
          </p>
        </motion.div>

        {/* Perfil Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card-academic p-8 mb-8"
        >
          <div className="flex items-start gap-6">
            <div className="text-6xl">{getPerfilIcon(resultado.perfil_risco)}</div>
            <div className="flex-1">
              <div className="inline-block px-3 py-1 bg-primary-50 text-primary text-xs font-semibold rounded-full mb-3">
                SEU PERFIL DE INVESTIDOR
              </div>
              <h2 className="text-2xl md:text-3xl font-bold text-academic-text mb-3">
                {resultado.perfil_risco}
              </h2>
              {resultado.justificativa && (
                <p className="text-academic-text-secondary leading-relaxed">
                  {resultado.justificativa}
                </p>
              )}
            </div>
          </div>
        </motion.div>

        {/* Explicabilidade e Confiança */}
        {resultado.explicabilidade && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="card-academic p-8 mb-8"
          >
            <h3 className="subsection-title mb-6">Por que chegamos a este perfil?</h3>

            <div className="grid md:grid-cols-2 gap-8 mb-6">
              {/* Confiança da Classificação */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="font-semibold text-academic-text">Confiança da Análise</span>
                  <span className="text-2xl font-bold text-primary">
                    {resultado.confianca_classificacao ? (resultado.confianca_classificacao * 100).toFixed(0) : '85'}%
                  </span>
                </div>
                <div className="w-full h-3 bg-academic-bg-secondary rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${resultado.confianca_classificacao ? resultado.confianca_classificacao * 100 : 85}%` }}
                    transition={{ duration: 1, delay: 0.3 }}
                    className="h-full bg-primary rounded-full"
                  />
                </div>
                <p className="text-xs text-academic-text-muted mt-2">
                  Nível de certeza do modelo de IA na classificação
                </p>
              </div>

              {/* Probabilidades de Perfis */}
              {resultado.probabilidades_perfis && (
                <div>
                  <div className="font-semibold text-academic-text mb-4">Distribuição de Probabilidade</div>
                  <div className="space-y-3">
                    {Object.entries(resultado.probabilidades_perfis)
                      .sort(([, a], [, b]) => b - a)
                      .map(([perfil, prob]) => (
                        <div key={perfil}>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="capitalize text-academic-text-secondary">{perfil}</span>
                            <span className="font-medium text-academic-text">{prob}%</span>
                          </div>
                          <div className="w-full h-2 bg-academic-bg-secondary rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${prob}%` }}
                              transition={{ duration: 0.8, delay: 0.4 }}
                              className={`h-full rounded-full ${
                                prob > 50 ? 'bg-primary' : 'bg-primary-light'
                              }`}
                            />
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </div>

            {/* Fatores Principais */}
            {resultado.explicabilidade.fatores_principais && resultado.explicabilidade.fatores_principais.length > 0 && (
              <div>
                <div className="font-semibold text-academic-text mb-4">Fatores que Influenciaram a Decisão</div>
                <div className="grid md:grid-cols-2 gap-4">
                  {resultado.explicabilidade.fatores_principais.map((fator, idx) => {
                    const impactoColor = {
                      positivo: 'text-success bg-green-50 border-green-200',
                      negativo: 'text-danger bg-red-50 border-red-200',
                      alerta: 'text-warning bg-yellow-50 border-yellow-200',
                      neutro: 'text-academic-text-secondary bg-gray-50 border-gray-200',
                    }[fator.impacto] || 'text-academic-text bg-academic-bg-secondary border-academic-border';

                    const impactoIcon = {
                      positivo: '↑',
                      negativo: '↓',
                      alerta: '⚠',
                      neutro: '→',
                    }[fator.impacto] || '•';

                    return (
                      <div key={idx} className={`border rounded-lg p-4 ${impactoColor}`}>
                        <div className="flex items-start gap-3">
                          <div className="text-2xl">{impactoIcon}</div>
                          <div>
                            <div className="font-medium text-sm mb-1">{fator.fator}</div>
                            <div className="text-xs opacity-75">
                              Peso na decisão: {(fator.peso * 100).toFixed(0)}%
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Análise de Sensibilidade */}
            {resultado.explicabilidade.sensibilidade && (
              <div className="mt-6 bg-academic-bg-secondary rounded-lg p-6">
                <div className="font-semibold text-academic-text mb-3 flex items-center gap-2">
                  <span>💡</span>
                  Análise de Sensibilidade
                </div>
                <div className="space-y-2 text-sm text-academic-text-secondary">
                  {Object.entries(resultado.explicabilidade.sensibilidade).map(([chave, valor]) => (
                    <div key={chave} className="flex items-start gap-2">
                      <span className="text-primary mt-0.5">•</span>
                      <span>
                        <strong className="text-academic-text">{chave.replace(/_/g, ' ').replace('se ', 'Se ')}:</strong> {valor}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}

        {/* Métricas Grid */}
        {resultado.metricas && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
          >
            {resultado.metricas.retorno_esperado_anual && (
              <div className="card-academic p-6">
                <div className="text-sm font-medium text-academic-text-secondary mb-2">
                  Retorno Esperado Anual
                </div>
                <div className="text-4xl font-bold text-success mb-2">
                  {resultado.metricas.retorno_esperado_anual}%
                </div>
                <div className="text-xs text-academic-text-muted">
                  Projeção baseada em dados históricos
                </div>
              </div>
            )}

            {resultado.metricas.risco_anual && (
              <div className="card-academic p-6">
                <div className="text-sm font-medium text-academic-text-secondary mb-2">
                  Volatilidade Anual
                </div>
                <div className="text-4xl font-bold text-warning mb-2">
                  {resultado.metricas.risco_anual}%
                </div>
                <div className="text-xs text-academic-text-muted">
                  Nível de oscilação esperado
                </div>
              </div>
            )}

            {resultado.metricas.sharpe_ratio && (
              <div className="card-academic p-6">
                <div className="text-sm font-medium text-academic-text-secondary mb-2">
                  Índice Sharpe
                </div>
                <div className="text-4xl font-bold text-primary mb-2">
                  {resultado.metricas.sharpe_ratio}
                </div>
                <div className="text-xs text-academic-text-muted">
                  {parseFloat(resultado.metricas.sharpe_ratio) > 1 ? 'Excelente relação risco/retorno' : 'Relação adequada'}
                </div>
              </div>
            )}
          </motion.div>
        )}

        {/* Alocação Section */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Gráfico de Pizza */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="card-academic p-8"
          >
            <h3 className="subsection-title mb-6">Distribuição da Carteira</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${value}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip
                  contentStyle={{
                    backgroundColor: '#FFFFFF',
                    border: '1px solid #E2E8F0',
                    borderRadius: '8px',
                  }}
                  formatter={(value) => [`${value}%`, 'Alocação']}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Detalhamento */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="card-academic p-8"
          >
            <h3 className="subsection-title mb-6">Detalhamento por Ativo</h3>
            <div className="space-y-4">
              {Object.entries(resultado.alocacao_recomendada || {}).map(([nome, valor], idx) => (
                <div key={nome}>
                  <div className="flex justify-between mb-2">
                    <span className="font-medium text-academic-text text-sm">{nome}</span>
                    <span className="font-bold text-primary">{valor}%</span>
                  </div>
                  <div className="w-full h-2 bg-academic-bg-secondary rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${valor}%` }}
                      transition={{ duration: 1, delay: 0.5 + idx * 0.1 }}
                      className="h-full rounded-full"
                      style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Projeção de Cenários */}
        {cenarios && cenarios.cenarios && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="card-academic p-8 mb-8"
          >
            <h3 className="subsection-title mb-6">Projeção de Cenários Futuros</h3>
            <p className="text-sm text-academic-text-secondary mb-6">
              Simulação de Monte Carlo com {cenarios.num_simulacoes || 1000} iterações, mostrando possíveis resultados da sua carteira.
            </p>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              {/* Cenário Pessimista */}
              <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg">
                <div className="text-sm font-medium text-red-700 mb-2">Cenário Pessimista (P10)</div>
                <div className="text-3xl font-bold text-red-600 mb-1">
                  R$ {cenarios.cenarios.pessimista?.valor_final_formatado || '0'}
                </div>
                <div className="text-xs text-red-600">
                  Retorno: {cenarios.cenarios.pessimista?.retorno_total_percentual || '0'}%
                </div>
                <div className="text-xs text-red-600 mt-1">
                  10% de chance de resultado pior que este
                </div>
              </div>

              {/* Cenário Realista */}
              <div className="bg-blue-50 border-l-4 border-primary p-6 rounded-lg">
                <div className="text-sm font-medium text-primary mb-2">Cenário Realista (P50)</div>
                <div className="text-3xl font-bold text-primary mb-1">
                  R$ {cenarios.cenarios.realista?.valor_final_formatado || '0'}
                </div>
                <div className="text-xs text-primary">
                  Retorno: {cenarios.cenarios.realista?.retorno_total_percentual || '0'}%
                </div>
                <div className="text-xs text-primary mt-1">
                  Resultado mais provável (mediana)
                </div>
              </div>

              {/* Cenário Otimista */}
              <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded-lg">
                <div className="text-sm font-medium text-green-700 mb-2">Cenário Otimista (P90)</div>
                <div className="text-3xl font-bold text-green-600 mb-1">
                  R$ {cenarios.cenarios.otimista?.valor_final_formatado || '0'}
                </div>
                <div className="text-xs text-green-600">
                  Retorno: {cenarios.cenarios.otimista?.retorno_total_percentual || '0'}%
                </div>
                <div className="text-xs text-green-600 mt-1">
                  10% de chance de resultado melhor que este
                </div>
              </div>
            </div>

            {/* Distribuição de Probabilidade */}
            {cenarios.metricas_risco && (
              <div className="bg-academic-bg-secondary rounded-lg p-6">
                <h4 className="font-semibold text-academic-text mb-4">Análise de Risco</h4>
                <div className="grid md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <div className="text-academic-text-muted mb-1">Valor Esperado</div>
                    <div className="font-bold text-academic-text">R$ {cenarios.metricas_risco.valor_esperado_formatado}</div>
                  </div>
                  <div>
                    <div className="text-academic-text-muted mb-1">Desvio Padrão</div>
                    <div className="font-bold text-academic-text">R$ {cenarios.metricas_risco.desvio_padrao_formatado}</div>
                  </div>
                  <div>
                    <div className="text-academic-text-muted mb-1">VaR 95%</div>
                    <div className="font-bold text-danger">R$ {cenarios.metricas_risco.var_95_formatado}</div>
                    <div className="text-xs text-academic-text-muted mt-1">Perda máxima esperada em 95% dos casos</div>
                  </div>
                  <div>
                    <div className="text-academic-text-muted mb-1">Prob. Lucro</div>
                    <div className="font-bold text-success">{cenarios.metricas_risco.probabilidade_lucro}%</div>
                    <div className="text-xs text-academic-text-muted mt-1">Chance de ter lucro</div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}

        {loadingCenarios && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="card-academic p-8 mb-8 text-center"
          >
            <div className="text-primary mb-2">Calculando cenários futuros...</div>
            <div className="text-sm text-academic-text-muted">Simulação de Monte Carlo em andamento</div>
          </motion.div>
        )}

        {/* Comparação com Benchmarks */}
        {benchmarks && benchmarks.comparacao && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.38 }}
            className="card-academic p-8 mb-8"
          >
            <h3 className="subsection-title mb-6">Comparação com Benchmarks</h3>
            <p className="text-sm text-academic-text-secondary mb-6">
              Comparação da performance da sua carteira personalizada com índices de mercado tradicionais.
              Período analisado: <strong>5 anos</strong> com aportes mensais.
            </p>

            <div className="grid md:grid-cols-4 gap-4 mb-6">
              {/* Sua Carteira */}
              <div className="bg-primary-50 border-2 border-primary p-4 rounded-lg">
                <div className="text-xs font-medium text-primary mb-2">Sua Carteira (IA)</div>
                <div className="text-2xl font-bold text-primary mb-1">
                  {benchmarks.comparacao.sua_carteira?.retorno_percentual || '0'}%
                </div>
                <div className="text-xs text-academic-text-secondary">
                  R$ {benchmarks.comparacao.sua_carteira?.valor_final_formatado || '0'}
                </div>
              </div>

              {/* CDI */}
              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border">
                <div className="text-xs font-medium text-academic-text mb-2">CDI (100%)</div>
                <div className="text-2xl font-bold text-academic-text mb-1">
                  {benchmarks.comparacao.cdi?.retorno_percentual || '0'}%
                </div>
                <div className="text-xs text-academic-text-secondary">
                  R$ {benchmarks.comparacao.cdi?.valor_final_formatado || '0'}
                </div>
                <div className={`text-xs font-medium mt-2 ${
                  parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                  parseFloat(benchmarks.comparacao.cdi?.retorno_percentual)
                  ? 'text-success' : 'text-danger'
                }`}>
                  {parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                   parseFloat(benchmarks.comparacao.cdi?.retorno_percentual)
                   ? '↑ ' : '↓ '}
                  {Math.abs(
                    parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual || 0) -
                    parseFloat(benchmarks.comparacao.cdi?.retorno_percentual || 0)
                  ).toFixed(1)}pp
                </div>
              </div>

              {/* IBOV */}
              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border">
                <div className="text-xs font-medium text-academic-text mb-2">IBOV</div>
                <div className="text-2xl font-bold text-academic-text mb-1">
                  {benchmarks.comparacao.ibov?.retorno_percentual || '0'}%
                </div>
                <div className="text-xs text-academic-text-secondary">
                  R$ {benchmarks.comparacao.ibov?.valor_final_formatado || '0'}
                </div>
                <div className={`text-xs font-medium mt-2 ${
                  parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                  parseFloat(benchmarks.comparacao.ibov?.retorno_percentual)
                  ? 'text-success' : 'text-danger'
                }`}>
                  {parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                   parseFloat(benchmarks.comparacao.ibov?.retorno_percentual)
                   ? '↑ ' : '↓ '}
                  {Math.abs(
                    parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual || 0) -
                    parseFloat(benchmarks.comparacao.ibov?.retorno_percentual || 0)
                  ).toFixed(1)}pp
                </div>
              </div>

              {/* S&P 500 */}
              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border">
                <div className="text-xs font-medium text-academic-text mb-2">S&P 500</div>
                <div className="text-2xl font-bold text-academic-text mb-1">
                  {benchmarks.comparacao.sp500?.retorno_percentual || '0'}%
                </div>
                <div className="text-xs text-academic-text-secondary">
                  R$ {benchmarks.comparacao.sp500?.valor_final_formatado || '0'}
                </div>
                <div className={`text-xs font-medium mt-2 ${
                  parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                  parseFloat(benchmarks.comparacao.sp500?.retorno_percentual)
                  ? 'text-success' : 'text-danger'
                }`}>
                  {parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                   parseFloat(benchmarks.comparacao.sp500?.retorno_percentual)
                   ? '↑ ' : '↓ '}
                  {Math.abs(
                    parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual || 0) -
                    parseFloat(benchmarks.comparacao.sp500?.retorno_percentual || 0)
                  ).toFixed(1)}pp
                </div>
              </div>
            </div>

            {/* Análise Comparativa */}
            <div className="bg-academic-bg-secondary rounded-lg p-6">
              <h4 className="font-semibold text-academic-text mb-4">Análise Comparativa</h4>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <div className="text-sm font-medium text-academic-text mb-3">Vantagens da Diversificação</div>
                  <ul className="space-y-2 text-sm text-academic-text-secondary">
                    <li className="flex items-start gap-2">
                      <span className="text-success mt-0.5">✓</span>
                      <span>Personalização baseada no seu perfil de risco</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-success mt-0.5">✓</span>
                      <span>Menor volatilidade através da diversificação</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-success mt-0.5">✓</span>
                      <span>Proteção contra quedas de setores específicos</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <div className="text-sm font-medium text-academic-text mb-3">Métricas de Performance</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-academic-text-secondary">Retorno/Risco (Sharpe)</span>
                      <span className="font-bold text-primary">{benchmarks.metricas?.sharpe_ratio || '1.2'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-academic-text-secondary">Melhor que CDI</span>
                      <span className="font-bold text-success">
                        {parseFloat(benchmarks.comparacao.sua_carteira?.retorno_percentual) >
                         parseFloat(benchmarks.comparacao.cdi?.retorno_percentual) ? 'Sim' : 'Não'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-academic-text-secondary">Diversificação</span>
                      <span className="font-bold text-primary">{Object.keys(resultado.alocacao_recomendada || {}).length} classes</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {loadingBenchmarks && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="card-academic p-8 mb-8 text-center"
          >
            <div className="text-primary mb-2">Comparando com benchmarks...</div>
            <div className="text-sm text-academic-text-muted">Analisando dados históricos do mercado</div>
          </motion.div>
        )}

        {/* Produtos Sugeridos */}
        {resultado.produtos_sugeridos && Object.keys(resultado.produtos_sugeridos).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card-academic p-8 mb-8"
          >
            <h3 className="subsection-title mb-6">Produtos Recomendados</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(resultado.produtos_sugeridos).map(([categoria, produtos]) => (
                <div key={categoria} className="bg-academic-bg-secondary p-4 rounded-lg">
                  <h4 className="font-semibold text-academic-text mb-3 capitalize">
                    {categoria.replace(/_/g, ' ')}
                  </h4>
                  <ul className="space-y-2">
                    {produtos.map((produto, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-academic-text-secondary">
                        <span className="text-success mt-0.5">✓</span>
                        <span>{produto}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Alertas */}
        {resultado.alertas && resultado.alertas.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-warning-light/10 border-l-4 border-warning p-6 rounded-lg mb-8"
          >
            <h3 className="font-semibold text-academic-text mb-3 flex items-center gap-2">
              <span className="text-warning">⚠️</span>
              Pontos de Atenção
            </h3>
            <ul className="space-y-2">
              {resultado.alertas.map((alerta, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm text-academic-text-secondary">
                  <span className="text-warning mt-0.5">•</span>
                  <span>{alerta}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        )}

        {/* Metodologia */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card-academic p-8 mb-8"
        >
          <h3 className="subsection-title mb-4">Metodologia Aplicada</h3>
          <p className="text-academic-text-secondary mb-6 text-sm leading-relaxed">
            Sua análise foi processada por uma <strong>Arquitetura Dual de Redes Neurais Ensemble</strong> com
            <strong> Voting Classifier (Rede 1)</strong> e <strong>Ensemble V4 Ultimate (Rede 2)</strong>,
            combinando 8 modelos heterogêneos de Machine Learning para máxima precisão e personalização.
          </p>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Rede 1 - Classificação */}
            <div className="bg-academic-bg-secondary p-4 rounded-lg">
              <h4 className="font-semibold text-academic-text mb-3 flex items-center gap-2">
                <span>🧠</span> Rede 1: Classificação de Perfil
              </h4>
              <div className="space-y-2 text-sm mb-3">
                <div className="flex justify-between">
                  <span className="text-academic-text-secondary">Random Forest</span>
                  <span className="font-medium">Peso 0.4</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-academic-text-secondary">MLP (15,10,5)</span>
                  <span className="font-medium">Peso 0.6</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-academic-text-secondary">SVM (RBF)</span>
                  <span className="font-medium">Arbitrador</span>
                </div>
              </div>
              <div className="bg-primary-50 p-3 rounded border border-primary">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-semibold text-primary">Acurácia</span>
                  <span className="text-2xl font-bold text-primary">88,2%</span>
                </div>
                <div className="text-xs text-academic-text-secondary mt-1">Soft Voting ponderado</div>
              </div>
            </div>

            {/* Rede 2 - Alocação */}
            <div className="bg-academic-bg-secondary p-4 rounded-lg">
              <h4 className="font-semibold text-academic-text mb-3 flex items-center gap-2">
                <span>💼</span> Rede 2: Alocação de Portfólio
              </h4>
              <div className="space-y-2 text-sm mb-3">
                <div className="flex justify-between">
                  <span className="text-academic-text-secondary">MLP1 (512,256,128,64)</span>
                  <span className="font-medium">Peso dinâmico</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-academic-text-secondary">MLP2 (400,200)</span>
                  <span className="font-medium">Peso dinâmico</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-academic-text-secondary">RF + GB + ET</span>
                  <span className="font-medium">3 modelos</span>
                </div>
              </div>
              <div className="bg-primary-50 p-3 rounded border border-primary">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-semibold text-primary">R² Score</span>
                  <span className="text-2xl font-bold text-primary">0,82</span>
                </div>
                <div className="text-xs text-academic-text-secondary mt-1">Feature Engineering 8→27</div>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="bg-academic-bg-secondary p-4 rounded-lg">
              <div className="font-semibold text-academic-text mb-1">Datasets</div>
              <div className="text-academic-text-muted text-xs">
                Risk Classifier (1.279) + Portfolio Allocator (5.000)
              </div>
            </div>
            <div className="bg-academic-bg-secondary p-4 rounded-lg">
              <div className="font-semibold text-academic-text mb-1">Latência</div>
              <div className="text-academic-text-muted text-xs">
                Análise completa em &lt;100ms (média)
              </div>
            </div>
            <div className="bg-academic-bg-secondary p-4 rounded-lg">
              <div className="font-semibold text-academic-text mb-1">Features</div>
              <div className="text-academic-text-muted text-xs">
                15 features (Rede 1) + 27 features (Rede 2)
              </div>
            </div>
          </div>
        </motion.div>

        {/* Validação Científica */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.65 }}
          className="card-academic p-8 mb-8"
        >
          <h3 className="subsection-title mb-4">Validação Científica do Modelo</h3>
          <p className="text-academic-text-secondary mb-6 text-sm leading-relaxed">
            Métricas de performance obtidas através de <strong>validação cruzada 5-fold estratificada</strong> e
            treinamento com datasets híbridos (Survey of Consumer Finances + dados sintéticos).
          </p>

          <div className="grid md:grid-cols-2 gap-8 mb-8">
            {/* Métricas de Classificação */}
            <div>
              <h4 className="font-semibold text-academic-text mb-4">Rede 1: Voting Classifier</h4>
              <div className="space-y-4">
                <div className="bg-academic-bg-secondary p-4 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-academic-text-secondary">Acurácia (Soft Voting)</span>
                    <span className="text-lg font-bold text-primary">88,2%</span>
                  </div>
                  <div className="text-xs text-academic-text-muted">100% dos erros entre classes adjacentes</div>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div className="bg-academic-bg-secondary p-3 rounded-lg text-center">
                    <div className="text-lg font-bold text-academic-text">88,0%</div>
                    <div className="text-xs text-academic-text-muted">Precisão</div>
                  </div>
                  <div className="bg-academic-bg-secondary p-3 rounded-lg text-center">
                    <div className="text-lg font-bold text-academic-text">88,2%</div>
                    <div className="text-xs text-academic-text-muted">Recall</div>
                  </div>
                  <div className="bg-academic-bg-secondary p-3 rounded-lg text-center">
                    <div className="text-lg font-bold text-academic-text">88,1%</div>
                    <div className="text-xs text-academic-text-muted">F1-Score</div>
                  </div>
                </div>

                <div className="bg-primary-50 p-4 rounded-lg border border-primary">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-academic-text">Confiança Média</span>
                    <span className="text-xl font-bold text-primary">70%</span>
                  </div>
                  <div className="text-xs text-academic-text-secondary">
                    Soft voting com pesos RF=0.4, MLP=0.6
                  </div>
                </div>
              </div>
            </div>

            {/* Métricas de Regressão */}
            <div>
              <h4 className="font-semibold text-academic-text mb-4">Rede 2: Ensemble V4 Ultimate</h4>
              <div className="space-y-4">
                <div className="bg-academic-bg-secondary p-4 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-academic-text-secondary">R² Score</span>
                    <span className="text-lg font-bold text-primary">0,82</span>
                  </div>
                  <div className="text-xs text-academic-text-muted">82% da variância explicada</div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-academic-bg-secondary p-3 rounded-lg text-center">
                    <div className="text-lg font-bold text-academic-text">+25,82pp</div>
                    <div className="text-xs text-academic-text-muted">Melhoria</div>
                    <div className="text-[10px] text-academic-text-muted mt-1">vs. V1 (R²=56%)</div>
                  </div>
                  <div className="bg-academic-bg-secondary p-3 rounded-lg text-center">
                    <div className="text-lg font-bold text-academic-text">5 modelos</div>
                    <div className="text-xs text-academic-text-muted">Ensemble</div>
                    <div className="text-[10px] text-academic-text-muted mt-1">Pesos dinâmicos</div>
                  </div>
                </div>

                <div className="bg-primary-50 p-4 rounded-lg border border-primary">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-academic-text">Feature Engineering</span>
                    <span className="text-xl font-bold text-primary">8→27</span>
                  </div>
                  <div className="text-xs text-academic-text-secondary">
                    Transformações polinomiais, logarítmicas e interações
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Características do Treinamento */}
          <div className="bg-academic-bg-secondary rounded-lg p-6">
            <h4 className="font-semibold text-academic-text mb-4">Características do Treinamento</h4>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-white p-4 rounded-lg">
                <div className="text-sm font-medium text-academic-text mb-2">Dataset Classificação</div>
                <div className="text-2xl font-bold text-primary mb-1">1.279</div>
                <div className="text-xs text-academic-text-muted">Registros (76% SCF + 24% sintético)</div>
              </div>

              <div className="bg-white p-4 rounded-lg">
                <div className="text-sm font-medium text-academic-text mb-2">Dataset Alocação</div>
                <div className="text-2xl font-bold text-primary mb-1">5.000</div>
                <div className="text-xs text-academic-text-muted">Amostras sintéticas balanceadas</div>
              </div>

              <div className="bg-white p-4 rounded-lg">
                <div className="text-sm font-medium text-academic-text mb-2">Validação</div>
                <div className="text-2xl font-bold text-primary mb-1">5-fold</div>
                <div className="text-xs text-academic-text-muted">Cross-validation estratificada</div>
              </div>
            </div>
          </div>

          <div className="mt-6 bg-primary-50 rounded-lg p-6 border border-primary">
            <p className="text-sm text-academic-text-secondary">
              <strong className="text-primary">Metodologia:</strong> Este sistema utiliza arquitetura dual de redes neurais
              ensemble, combinando Voting Classifier (classificação) com Ensemble V4 Ultimate (alocação), aplicando
              feature engineering agressivo e fallback inteligente baseado em perfil de risco para garantir recomendações
              sempre válidas e diversificadas.
            </p>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="flex flex-col sm:flex-row gap-4 justify-center mb-8"
        >
          <button
            onClick={handleNovaAnalise}
            className="btn-primary px-8 py-3"
          >
            Nova Análise
          </button>
          <button
            onClick={() => window.print()}
            className="btn-secondary px-8 py-3"
          >
            Imprimir Relatório
          </button>
          <Link to="/">
            <button className="btn-secondary px-8 py-3 w-full sm:w-auto">
              Voltar ao Início
            </button>
          </Link>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="bg-academic-bg-secondary border border-academic-border rounded-lg p-6 text-center"
        >
          <p className="text-sm text-academic-text-secondary">
            <strong className="text-academic-text">Aviso Importante:</strong> Este sistema foi desenvolvido para fins
            acadêmicos (TCC - Sistemas de Informação). As recomendações são baseadas em modelos de IA e não constituem
            aconselhamento financeiro profissional. Sempre consulte um assessor certificado antes de investir.
          </p>
        </motion.div>
      </div>
    </div>
  );
}
