import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { simularBacktesting, compararBenchmarks, cenariosDetalhados } from '../services/api';
import Loading from '../components/Loading';

export default function Simulacao() {
  const navigate = useNavigate();
  const [alocacao, setAlocacao] = useState(null);
  const [dadosUsuario, setDadosUsuario] = useState(null);

  // Estado de carregamento
  const [carregandoInicial, setCarregandoInicial] = useState(true);
  const [simulando, setSimulando] = useState(false);

  // Dados das simulações
  const [backtest, setBacktest] = useState(null);
  const [comparacao, setComparacao] = useState(null);
  const [cenarios, setCenarios] = useState(null);

  // Parâmetros AJUSTÁVEIS pelo usuário
  const [valorInicial, setValorInicial] = useState(10000);
  const [aporteMensal, setAporteMensal] = useState(500);
  const [periodo, setPeriodo] = useState('5y');
  const [anos, setAnos] = useState(10);

  // Carregar dados do usuário do localStorage
  useEffect(() => {
    const resultado = localStorage.getItem('resultado_investimento');
    const formulario = localStorage.getItem('dados_formulario');

    if (!resultado) {
      navigate('/questionario');
      return;
    }

    const dataResultado = JSON.parse(resultado);
    setAlocacao(dataResultado.alocacao_recomendada);

    // Carregar dados do formulário do usuário
    if (formulario) {
      const dataForm = JSON.parse(formulario);
      setDadosUsuario(dataForm);

      // Inicializar com os valores REAIS do usuário
      setValorInicial(dataForm.valor_investir_mensal || 10000);
      setAporteMensal(dataForm.valor_investir_mensal || 500);
    }

    setCarregandoInicial(false);
  }, [navigate]);

  // Executar simulação inicial após carregar dados
  useEffect(() => {
    if (alocacao && !carregandoInicial) {
      executarSimulacoes();
    }
  }, [alocacao, carregandoInicial]);

  const executarSimulacoes = async () => {
    setSimulando(true);

    try {
      const dadosSimulacao = {
        alocacao: alocacao,
        valor_inicial: valorInicial,
        aporte_mensal: aporteMensal,
        periodo: periodo
      };

      // Executar todas as simulações em paralelo
      const [backtestResult, comparacaoResult, cenariosResult] = await Promise.all([
        simularBacktesting(dadosSimulacao),
        compararBenchmarks(dadosSimulacao),
        cenariosDetalhados({
          alocacao: alocacao,
          valor_inicial: valorInicial,
          aporte_mensal: aporteMensal,
          anos: anos
        })
      ]);

      setBacktest(backtestResult);
      setComparacao(comparacaoResult);
      setCenarios(cenariosResult);
      setSimulando(false);

    } catch (error) {
      console.error('Erro na simulação:', error);
      setSimulando(false);
      alert('Erro ao executar simulação. Verifique sua conexão e tente novamente.');
    }
  };

  const formatarMoeda = (valor) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(valor);
  };

  const formatarPercentual = (valor) => {
    return `${valor.toFixed(2)}%`;
  };

  // Loading inicial (carregando dados do usuário)
  if (carregandoInicial) {
    return (
      <div className="container mx-auto px-4 py-12">
        <Loading message="Carregando seus dados..." />
      </div>
    );
  }

  // Preparar dados para gráficos
  const dadosBacktest = backtest?.datas?.map((data, idx) => ({
    mes: idx,
    data: new Date(data).toLocaleDateString('pt-BR', { month: 'short', year: '2-digit' }),
    patrimonio: backtest.patrimonio_historico[idx]
  })) || [];

  const dadosComparacao = comparacao ? [
    {
      nome: 'Sua Carteira IA',
      final: comparacao.carteira_ia.patrimonio_final,
      retorno: comparacao.carteira_ia.retorno_anualizado
    },
    ...Object.entries(comparacao.benchmarks).map(([nome, dados]) => ({
      nome,
      final: dados.patrimonio_final,
      retorno: dados.retorno_anualizado
    }))
  ] : [];

  const dadosCenarios = cenarios?.meses?.map((mes, idx) => ({
    mes,
    otimista: cenarios.otimista.patrimonio[idx],
    realista: cenarios.realista.patrimonio[idx],
    pessimista: cenarios.pessimista.patrimonio[idx]
  })) || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/resultado')}
            className="text-blue-600 hover:text-blue-700 mb-4 flex items-center"
          >
            ← Voltar para Resultados
          </button>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Simulador Avançado
          </h1>
          <p className="text-gray-600">
            Simule sua carteira com dados reais do mercado brasileiro
          </p>
        </div>

        {/* Painel de Controles Interativos */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            🎛️ Ajuste os Parâmetros da Simulação
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Valor Inicial */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Valor Inicial
              </label>
              <input
                type="number"
                value={valorInicial}
                onChange={(e) => setValorInicial(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                min="100"
                step="100"
              />
              <p className="text-xs text-gray-500 mt-1">
                {formatarMoeda(valorInicial)}
              </p>
            </div>

            {/* Aporte Mensal */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Aporte Mensal
              </label>
              <input
                type="number"
                value={aporteMensal}
                onChange={(e) => setAporteMensal(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                min="0"
                step="50"
              />
              <p className="text-xs text-gray-500 mt-1">
                {formatarMoeda(aporteMensal)}
              </p>
            </div>

            {/* Período Histórico */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Período Histórico
              </label>
              <select
                value={periodo}
                onChange={(e) => setPeriodo(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
              >
                <option value="1y">1 ano</option>
                <option value="2y">2 anos</option>
                <option value="5y">5 anos</option>
                <option value="10y">10 anos</option>
              </select>
            </div>

            {/* Anos de Projeção */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Projeção Futura
              </label>
              <select
                value={anos}
                onChange={(e) => setAnos(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
              >
                <option value="5">5 anos</option>
                <option value="10">10 anos</option>
                <option value="15">15 anos</option>
                <option value="20">20 anos</option>
                <option value="30">30 anos</option>
              </select>
            </div>
          </div>

          {/* Botão de Simular */}
          <div className="mt-6 flex justify-center">
            <button
              onClick={executarSimulacoes}
              disabled={simulando}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-lg hover:shadow-xl transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {simulando ? '⏳ Simulando...' : '🚀 Simular Novamente'}
            </button>
          </div>
        </div>

        {/* Loading de Simulação */}
        {simulando && (
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <Loading message="Executando simulação com dados reais do mercado..." />
            <p className="text-center text-gray-600 mt-4">
              Baixando cotações históricas e executando Monte Carlo (1000+ cenários)...
            </p>
          </div>
        )}

        {/* Resultados */}
        {!simulando && backtest && comparacao && cenarios && (
          <>
            {/* Métricas Principais */}
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-sm text-gray-600 mb-1">Patrimônio Final</div>
                <div className="text-2xl font-bold text-green-600">
                  {formatarMoeda(backtest.patrimonio_final)}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Total aportado: {formatarMoeda(backtest.total_aportado)}
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-sm text-gray-600 mb-1">Retorno Anualizado</div>
                <div className="text-2xl font-bold text-blue-600">
                  {formatarPercentual(backtest.retorno_anualizado)}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Rentabilidade: {formatarPercentual(backtest.rentabilidade_total)}
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-sm text-gray-600 mb-1">Sharpe Ratio</div>
                <div className="text-2xl font-bold text-purple-600">
                  {backtest.sharpe_ratio.toFixed(2)}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Volatilidade: {formatarPercentual(backtest.volatilidade_anual)}
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="text-sm text-gray-600 mb-1">Maior Queda</div>
                <div className="text-2xl font-bold text-red-600">
                  {formatarPercentual(backtest.max_drawdown)}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Melhor mês: {formatarPercentual(backtest.melhor_mes)}
                </div>
              </div>
            </div>

            {/* Gráfico 1: Evolução Histórica */}
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                📈 Evolução Patrimonial (Dados Históricos Reais)
              </h2>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={dadosBacktest}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="data" />
                  <YAxis tickFormatter={(value) => formatarMoeda(value)} />
                  <Tooltip
                    formatter={(value) => formatarMoeda(value)}
                    labelFormatter={(label) => `Data: ${label}`}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="patrimonio"
                    stroke="#0066FF"
                    strokeWidth={3}
                    name="Seu Patrimônio"
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Gráfico 2: Comparação com Benchmarks */}
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                🏆 Comparação com Benchmarks do Mercado
              </h2>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={dadosComparacao}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="nome" />
                  <YAxis tickFormatter={(value) => formatarMoeda(value)} />
                  <Tooltip formatter={(value) => formatarMoeda(value)} />
                  <Legend />
                  <Bar dataKey="final" fill="#0066FF" name="Patrimônio Final" />
                </BarChart>
              </ResponsiveContainer>

              {/* Tabela de Detalhes */}
              <div className="mt-6 overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-100">
                    <tr>
                      <th className="px-4 py-2 text-left">Benchmark</th>
                      <th className="px-4 py-2 text-right">Patrimônio Final</th>
                      <th className="px-4 py-2 text-right">Retorno Anualizado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dadosComparacao.map((item, idx) => (
                      <tr key={idx} className={idx === 0 ? 'bg-blue-50 font-bold' : ''}>
                        <td className="px-4 py-2">{item.nome}</td>
                        <td className="px-4 py-2 text-right">{formatarMoeda(item.final)}</td>
                        <td className="px-4 py-2 text-right">{formatarPercentual(item.retorno)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Gráfico 3: Cenários Futuros */}
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                🔮 Projeções Futuras ({anos} anos) - Monte Carlo
              </h2>
              <p className="text-gray-600 mb-4">
                1000+ simulações probabilísticas baseadas em dados históricos
              </p>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={dadosCenarios}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="mes" label={{ value: 'Meses', position: 'insideBottom', offset: -5 }} />
                  <YAxis tickFormatter={(value) => formatarMoeda(value)} />
                  <Tooltip formatter={(value) => formatarMoeda(value)} />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="otimista"
                    stackId="1"
                    stroke="#10b981"
                    fill="#86efac"
                    name="Cenário Otimista"
                  />
                  <Area
                    type="monotone"
                    dataKey="realista"
                    stackId="2"
                    stroke="#3b82f6"
                    fill="#93c5fd"
                    name="Cenário Realista"
                  />
                  <Area
                    type="monotone"
                    dataKey="pessimista"
                    stackId="3"
                    stroke="#ef4444"
                    fill="#fca5a5"
                    name="Cenário Pessimista"
                  />
                </AreaChart>
              </ResponsiveContainer>

              {/* Cards de Cenários */}
              <div className="grid md:grid-cols-3 gap-4 mt-6">
                <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                  <div className="text-sm text-green-700 font-semibold mb-1">Cenário Otimista</div>
                  <div className="text-2xl font-bold text-green-600">
                    {formatarMoeda(cenarios.otimista.final)}
                  </div>
                  <div className="text-xs text-green-600 mt-1">Mercado favorável</div>
                </div>

                <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
                  <div className="text-sm text-blue-700 font-semibold mb-1">Cenário Realista</div>
                  <div className="text-2xl font-bold text-blue-600">
                    {formatarMoeda(cenarios.realista.final)}
                  </div>
                  <div className="text-xs text-blue-600 mt-1">Expectativa mais provável</div>
                </div>

                <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
                  <div className="text-sm text-red-700 font-semibold mb-1">Cenário Pessimista</div>
                  <div className="text-2xl font-bold text-red-600">
                    {formatarMoeda(cenarios.pessimista.final)}
                  </div>
                  <div className="text-xs text-red-600 mt-1">Mercado desfavorável</div>
                </div>
              </div>
            </div>

            {/* Informações Adicionais */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
              <h3 className="text-xl font-bold mb-3">ℹ️ Sobre esta Simulação</h3>
              <ul className="space-y-2 text-sm">
                <li>✓ <strong>Dados Reais:</strong> Cotações do mercado brasileiro via Yahoo Finance (BOVA11, IVVB11, IFIX, etc.)</li>
                <li>✓ <strong>Backtesting:</strong> Simulação com preços históricos reais do período selecionado</li>
                <li>✓ <strong>Monte Carlo:</strong> 1000+ cenários probabilísticos para projeção futura</li>
                <li>✓ <strong>Benchmarks:</strong> Comparação com CDI, IBOVESPA e S&P 500</li>
                <li>⚠️ <strong>Aviso:</strong> Rentabilidade passada não garante resultados futuros</li>
              </ul>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
