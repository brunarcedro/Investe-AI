import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

export default function Resultado() {
  const navigate = useNavigate();
  const [resultado, setResultado] = useState(null);

  useEffect(() => {
    // Carregar resultado do localStorage
    const data = localStorage.getItem('resultado_investimento');
    if (data) {
      setResultado(JSON.parse(data));
    } else {
      // Se não houver resultado, redirecionar para questionário
      navigate('/questionario');
    }
  }, [navigate]);

  if (!resultado) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="text-center">
          <p>Carregando resultado...</p>
        </div>
      </div>
    );
  }

  // Preparar dados para o gráfico de pizza
  const chartData = Object.entries(resultado.alocacao_recomendada || {}).map(
    ([nome, valor]) => ({
      name: nome,
      value: parseFloat(valor),
    })
  );

  // Cores para o gráfico
  const COLORS = ['#0066FF', '#00C853', '#FFD700', '#FF3D00', '#9C27B0', '#FF9800'];

  // Função para determinar a cor do perfil
  const getPerfilColor = (perfil) => {
    if (perfil.includes('Conservador')) return 'text-blue-600';
    if (perfil.includes('Moderado')) return 'text-yellow-600';
    if (perfil.includes('Arrojado')) return 'text-red-600';
    return 'text-gray-600';
  };

  const handleNovaAnalise = () => {
    localStorage.removeItem('resultado_investimento');
    navigate('/questionario');
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary to-blue-600 text-white rounded-lg p-8 mb-8">
        <h1 className="text-4xl font-bold mb-2">Sua Carteira Personalizada</h1>
        <p className="text-xl opacity-90">
          Recomendações geradas por Inteligência Artificial
        </p>
      </div>

      {/* Perfil de Risco */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold mb-4">Seu Perfil de Investidor</h2>
        <div className="flex items-center space-x-4">
          <div className={`text-5xl font-bold ${getPerfilColor(resultado.perfil_risco)}`}>
            {resultado.perfil_risco}
          </div>
        </div>
        {resultado.justificativa && (
          <p className="text-gray-700 mt-4 leading-relaxed">{resultado.justificativa}</p>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* Gráfico de Alocação */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-6">Alocação Recomendada</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Métricas */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-6">Métricas Financeiras</h2>
          <div className="space-y-4">
            {resultado.metricas?.retorno_esperado_anual && (
              <div className="border-l-4 border-green-500 pl-4">
                <div className="text-sm text-gray-600">Retorno Esperado Anual</div>
                <div className="text-3xl font-bold text-green-600">
                  {resultado.metricas.retorno_esperado_anual}%
                </div>
              </div>
            )}

            {resultado.metricas?.risco_anual && (
              <div className="border-l-4 border-orange-500 pl-4">
                <div className="text-sm text-gray-600">Risco Anual (Volatilidade)</div>
                <div className="text-3xl font-bold text-orange-600">
                  {resultado.metricas.risco_anual}%
                </div>
              </div>
            )}

            {resultado.metricas?.sharpe_ratio && (
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="text-sm text-gray-600">Índice Sharpe</div>
                <div className="text-3xl font-bold text-blue-600">
                  {resultado.metricas.sharpe_ratio}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Quanto maior, melhor o retorno ajustado ao risco
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Produtos Sugeridos */}
      {resultado.produtos_sugeridos && Object.keys(resultado.produtos_sugeridos).length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-6">Produtos Sugeridos</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {Object.entries(resultado.produtos_sugeridos).map(([categoria, produtos]) => (
              <div key={categoria} className="border rounded-lg p-4">
                <h3 className="font-bold mb-3 text-lg capitalize">
                  {categoria.replace('_', ' ')}
                </h3>
                <ul className="space-y-2">
                  {produtos.map((produto, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-gray-700">{produto}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Alertas */}
      {resultado.alertas && resultado.alertas.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold mb-4 text-yellow-800">⚠️ Alertas e Recomendações</h2>
          <ul className="space-y-2">
            {resultado.alertas.map((alerta, idx) => (
              <li key={idx} className="text-yellow-800">
                {alerta}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Detalhamento da Alocação */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold mb-6">Detalhamento da Alocação</h2>
        <div className="space-y-3">
          {Object.entries(resultado.alocacao_recomendada || {}).map(([nome, valor], idx) => (
            <div key={nome} className="flex items-center">
              <div className="flex-grow">
                <div className="flex justify-between mb-1">
                  <span className="font-medium">{nome}</span>
                  <span className="font-bold text-primary">{valor}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="h-3 rounded-full transition-all"
                    style={{
                      width: `${valor}%`,
                      backgroundColor: COLORS[idx % COLORS.length],
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Ações */}
      <div className="flex flex-col md:flex-row gap-4 justify-center">
        <Link
          to="/simulacao"
          className="px-8 py-3 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition text-center shadow-lg transform hover:scale-105"
        >
          📊 Ver Simulação com Dados Reais
        </Link>

        <button
          onClick={handleNovaAnalise}
          className="px-8 py-3 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 transition"
        >
          🔄 Nova Análise
        </button>

        <button
          onClick={() => window.print()}
          className="px-8 py-3 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition"
        >
          🖨️ Imprimir Resultado
        </button>

        <Link
          to="/"
          className="px-8 py-3 bg-secondary text-white rounded-lg font-medium hover:bg-green-600 transition text-center"
        >
          🏠 Voltar ao Início
        </Link>
      </div>

      {/* Disclaimer */}
      <div className="mt-8 bg-gray-50 border border-gray-200 rounded-lg p-6">
        <p className="text-sm text-gray-600 text-center">
          <strong>Aviso:</strong> Este é um sistema de recomendação educacional desenvolvido como TCC.
          As recomendações são baseadas em modelos de IA e não constituem aconselhamento financeiro.
          Sempre consulte um profissional certificado antes de investir.
        </p>
      </div>
    </div>
  );
}
