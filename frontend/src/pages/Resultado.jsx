import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip as RechartsTooltip } from 'recharts';

export default function Resultado() {
  const navigate = useNavigate();
  const [resultado, setResultado] = useState(null);
  const [xp, setXp] = useState(0);
  const [showConquista, setShowConquista] = useState(false);
  const [countUpValues, setCountUpValues] = useState({
    retorno: 0,
    risco: 0,
    sharpe: 0,
  });

  useEffect(() => {
    // Carregar resultado do localStorage
    const data = localStorage.getItem('resultado_investimento');
    if (data) {
      setResultado(JSON.parse(data));
    } else {
      navigate('/questionario');
    }

    // Carregar XP
    const xpConquistado = localStorage.getItem('xp_conquistado');
    if (xpConquistado) {
      const xpAtual = parseInt(xpConquistado);
      setXp(xpAtual);

      // Add completion bonus
      const novoXp = xpAtual + 40;
      setXp(novoXp);
      localStorage.setItem('xp_conquistado', novoXp);

      // Show conquista
      setShowConquista(true);
      setTimeout(() => setShowConquista(false), 5000);
    }
  }, [navigate]);

  // CountUp animation effect
  useEffect(() => {
    if (resultado?.metricas) {
      const duration = 2000; // 2 seconds
      const steps = 60;
      const interval = duration / steps;

      const targetRetorno = resultado.metricas.retorno_esperado_anual || 0;
      const targetRisco = resultado.metricas.risco_anual || 0;
      const targetSharpe = resultado.metricas.sharpe_ratio || 0;

      let currentStep = 0;

      const timer = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;

        setCountUpValues({
          retorno: (targetRetorno * progress).toFixed(1),
          risco: (targetRisco * progress).toFixed(1),
          sharpe: (targetSharpe * progress).toFixed(2),
        });

        if (currentStep >= steps) {
          clearInterval(timer);
          setCountUpValues({
            retorno: targetRetorno,
            risco: targetRisco,
            sharpe: targetSharpe,
          });
        }
      }, interval);

      return () => clearInterval(timer);
    }
  }, [resultado]);

  // Tooltip Component
  const Tooltip = ({ text }) => (
    <div className="group relative inline-block ml-2">
      <span className="text-primary cursor-help text-sm">ℹ️</span>
      <div className="invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-300 absolute z-50 w-64 p-3 bg-dark-hover border border-primary/30 rounded-lg shadow-premium text-sm text-dark-text -left-28 top-6">
        <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-dark-hover border-l border-t border-primary/30 rotate-45"></div>
        {text}
      </div>
    </div>
  );

  if (!resultado) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="text-6xl mb-6 animate-spin">📊</div>
          <p className="text-xl text-dark-text">Carregando resultado...</p>
        </motion.div>
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

  // Cores dark theme para o gráfico
  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

  // Função para determinar estilo do perfil (dark theme)
  const getPerfilStyle = (perfil) => {
    if (perfil.includes('Conservador')) {
      return {
        color: 'text-blue-400',
        gradient: 'from-blue-500 to-cyan-500',
        icon: '🛡️',
        badge: 'bg-blue-500/20 border-blue-500/50',
      };
    }
    if (perfil.includes('Moderado')) {
      return {
        color: 'text-warning',
        gradient: 'from-warning to-orange-500',
        icon: '⚖️',
        badge: 'bg-warning/20 border-warning/50',
      };
    }
    if (perfil.includes('Arrojado')) {
      return {
        color: 'text-danger',
        gradient: 'from-danger to-pink-500',
        icon: '🚀',
        badge: 'bg-danger/20 border-danger/50',
      };
    }
    return {
      color: 'text-primary',
      gradient: 'from-primary to-gradient-cyan',
      icon: '📊',
      badge: 'bg-primary/20 border-primary/50',
    };
  };

  const style = getPerfilStyle(resultado.perfil_risco);

  const handleNovaAnalise = () => {
    localStorage.removeItem('resultado_investimento');
    localStorage.removeItem('perfil_investidor');
    localStorage.removeItem('dados_formulario');
    localStorage.removeItem('xp_conquistado');
    navigate('/questionario');
  };

  // Calculate investor level
  const getNivel = (xp) => {
    if (xp >= 100) return { nome: 'Especialista', icon: '💎', color: 'text-gradient-cyan' };
    if (xp >= 75) return { nome: 'Avançado', icon: '🥇', color: 'text-warning' };
    if (xp >= 50) return { nome: 'Intermediário', icon: '🥈', color: 'text-gray-400' };
    return { nome: 'Iniciante', icon: '🥉', color: 'text-orange-400' };
  };

  const nivel = getNivel(xp);

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-7xl">
        {/* Conquista Banner */}
        <AnimatePresence>
          {showConquista && (
            <motion.div
              initial={{ opacity: 0, y: -50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50 glass-card px-8 py-4 border-2 border-success"
            >
              <div className="flex items-center gap-4">
                <div className="text-4xl animate-bounce">🏆</div>
                <div>
                  <div className="text-success font-bold text-lg">Nova Conquista!</div>
                  <div className="text-dark-muted">+40 XP - Carteira Completa Gerada</div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Header com XP */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4"
        >
          <div>
            <h1 className="text-4xl md:text-5xl font-bold text-dark-text mb-2">
              Sua Carteira Personalizada
            </h1>
            <p className="text-dark-muted text-lg">
              Recomendações geradas por IA com base no seu perfil
            </p>
          </div>

          {/* XP Badge */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="glass-card px-6 py-4 text-center border-2 border-success"
          >
            <div className="text-3xl mb-1">{nivel.icon}</div>
            <div className={`text-sm font-bold ${nivel.color}`}>{nivel.nome}</div>
            <div className="text-2xl font-bold text-success">{xp} XP</div>
          </motion.div>
        </motion.div>

        {/* Hero Card - Perfil */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="relative overflow-hidden rounded-2xl mb-8"
        >
          <div className={`absolute inset-0 bg-gradient-to-br ${style.gradient} opacity-20`} />

          <div className="relative glass-card p-8">
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="text-7xl">{style.icon}</div>

              <div className="flex-1 text-center md:text-left">
                <div className={`inline-block px-4 py-2 ${style.badge} border rounded-full mb-3`}>
                  <span className="text-sm font-bold text-dark-text">SEU PERFIL</span>
                </div>

                <h2 className={`text-4xl md:text-5xl font-bold mb-3 bg-gradient-to-r ${style.gradient} bg-clip-text text-transparent`}>
                  {resultado.perfil_risco}
                </h2>

                {resultado.justificativa && (
                  <p className="text-dark-muted text-lg leading-relaxed">
                    {resultado.justificativa}
                  </p>
                )}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Métricas Principais - Cards */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          {/* Retorno Esperado */}
          {resultado.metricas?.retorno_esperado_anual && (
            <div className="card-hover border-l-4 border-success group">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="text-dark-muted text-sm mb-2 flex items-center">
                    RETORNO ESPERADO ANUAL
                    <Tooltip text="Ganho percentual médio esperado por ano, baseado em histórico de mercado e perfil de risco." />
                  </div>
                  <div className="text-5xl font-bold text-success mb-1">
                    {countUpValues.retorno}%
                  </div>
                  <div className="text-sm text-dark-muted">
                    Projeção baseada em histórico
                  </div>
                </div>
                <div className="text-5xl group-hover:scale-110 transition-transform">💵</div>
              </div>
            </div>
          )}

          {/* Risco/Volatilidade */}
          {resultado.metricas?.risco_anual && (
            <div className="card-hover border-l-4 border-warning group">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="text-dark-muted text-sm mb-2 flex items-center">
                    VOLATILIDADE ANUAL
                    <Tooltip text="Medida de variação dos preços. Indica o quanto seus investimentos podem oscilar ao longo do ano." />
                  </div>
                  <div className="text-5xl font-bold text-warning mb-1">
                    {countUpValues.risco}%
                  </div>
                  <div className="text-sm text-dark-muted">
                    Nível de oscilação esperado
                  </div>
                </div>
                <div className="text-5xl group-hover:scale-110 transition-transform">⚠️</div>
              </div>
            </div>
          )}

          {/* Sharpe Ratio */}
          {resultado.metricas?.sharpe_ratio && (
            <div className="card-hover border-l-4 border-primary group">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="text-dark-muted text-sm mb-2 flex items-center">
                    ÍNDICE SHARPE
                    <Tooltip text="Retorno ajustado ao risco. Valores acima de 1 são considerados bons, acima de 2 são excelentes." />
                  </div>
                  <div className="text-5xl font-bold text-primary mb-1">
                    {countUpValues.sharpe}
                  </div>
                  <div className="text-sm text-dark-muted">
                    {parseFloat(countUpValues.sharpe) > 1 ? 'Excelente relação risco/retorno' : 'Relação risco/retorno adequada'}
                  </div>
                </div>
                <div className="text-5xl group-hover:scale-110 transition-transform">📊</div>
              </div>
            </div>
          )}
        </motion.div>

        {/* Gráfico e Alocação Detalhada - 2 Colunas */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Gráfico de Pizza */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="glass-card p-8"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">🥧</div>
              <h3 className="text-2xl font-bold text-dark-text">Alocação Visual</h3>
            </div>

            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${value}%`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="value"
                  animationBegin={0}
                  animationDuration={1000}
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip
                  contentStyle={{
                    backgroundColor: '#151A36',
                    border: '1px solid #2A3154',
                    borderRadius: '8px',
                    color: '#E5E7EB',
                  }}
                  formatter={(value) => [`${value}%`, 'Alocação']}
                />
                <Legend
                  wrapperStyle={{
                    color: '#E5E7EB',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Detalhamento com Barras */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="glass-card p-8"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">📈</div>
              <h3 className="text-2xl font-bold text-dark-text">Detalhamento</h3>
            </div>

            <div className="space-y-4">
              {Object.entries(resultado.alocacao_recomendada || {}).map(([nome, valor], idx) => (
                <motion.div
                  key={nome}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + idx * 0.1 }}
                >
                  <div className="flex justify-between mb-2">
                    <span className="font-medium text-dark-text">{nome}</span>
                    <span className="font-bold text-primary text-lg">{valor}%</span>
                  </div>
                  <div className="w-full h-3 bg-dark-hover rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${valor}%` }}
                      transition={{ duration: 1, delay: 0.8 + idx * 0.1 }}
                      className="h-full rounded-full"
                      style={{
                        backgroundColor: COLORS[idx % COLORS.length],
                      }}
                    />
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Produtos Sugeridos */}
        {resultado.produtos_sugeridos && Object.keys(resultado.produtos_sugeridos).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="glass-card p-8 mb-8"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">💼</div>
              <h3 className="text-2xl font-bold text-dark-text">Produtos Recomendados</h3>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(resultado.produtos_sugeridos).map(([categoria, produtos], catIdx) => (
                <motion.div
                  key={categoria}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.9 + catIdx * 0.1 }}
                  className="card-hover"
                >
                  <h4 className="font-bold mb-4 text-lg text-primary capitalize flex items-center gap-2">
                    <span>→</span>
                    {categoria.replace(/_/g, ' ')}
                  </h4>
                  <ul className="space-y-2">
                    {produtos.map((produto, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-dark-muted">
                        <span className="text-success text-lg flex-shrink-0">✓</span>
                        <span>{produto}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Alertas */}
        {resultado.alertas && resultado.alertas.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1 }}
            className="glass-card p-8 mb-8 border-l-4 border-warning"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">⚠️</div>
              <h3 className="text-2xl font-bold text-warning">Alertas Importantes</h3>
            </div>

            <ul className="space-y-3">
              {resultado.alertas.map((alerta, idx) => (
                <motion.li
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1.1 + idx * 0.1 }}
                  className="flex items-start gap-3"
                >
                  <span className="text-warning text-xl flex-shrink-0">•</span>
                  <span className="text-dark-muted">{alerta}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>
        )}

        {/* Como Foi Calculado - Stacking Ensemble */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          className="glass-card p-8 mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="text-4xl">🤖</div>
            <h3 className="text-2xl font-bold text-dark-text">Como Foi Calculado?</h3>
          </div>

          <p className="text-dark-muted mb-6">
            Seu perfil foi analisado por um sistema de <strong className="text-primary">Arquitetura Dual de Redes Neurais</strong> utilizando
            <strong className="text-success"> Stacking Ensemble com 7 modelos</strong> de Machine Learning trabalhando em conjunto:
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            {[
              { nome: 'MLP 1', acc: '88,3%', desc: 'Rede Neural (100,50)', color: 'border-blue-500' },
              { nome: 'MLP 2', acc: '86,7%', desc: 'Rede Neural (50,25)', color: 'border-cyan-500' },
              { nome: 'Random Forest', acc: '87,1%', desc: '100 árvores', color: 'border-green-500' },
              { nome: 'Gradient Boosting', acc: '88,9%', desc: 'Boosting otimizado', color: 'border-yellow-500' },
              { nome: 'XGBoost', acc: '89,2%', desc: 'Melhor modelo base', color: 'border-orange-500' },
              { nome: 'LightGBM', acc: '88,5%', desc: 'Boosting rápido', color: 'border-purple-500' },
              { nome: 'Extra Trees', acc: '86,9%', desc: 'Árvores extras', color: 'border-pink-500' },
            ].map((modelo, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1.1 + idx * 0.05 }}
                className={`card-hover border-l-4 ${modelo.color} text-center`}
              >
                <div className="text-2xl font-bold text-primary mb-1">{modelo.acc}</div>
                <div className="text-sm font-bold text-dark-text mb-1">{modelo.nome}</div>
                <div className="text-xs text-dark-muted">{modelo.desc}</div>
              </motion.div>
            ))}

            {/* Meta-Modelo (Resultado Final) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.45 }}
              className="card-hover border-2 border-success bg-gradient-to-br from-success/10 to-primary/10"
            >
              <div className="text-3xl font-bold text-success mb-1">91,5%</div>
              <div className="text-sm font-bold text-dark-text mb-1">🏆 Stacking</div>
              <div className="text-xs text-dark-muted">Meta-modelo final</div>
              <div className="text-[10px] text-success mt-1">IC 95%: [91,0%, 92,0%]</div>
            </motion.div>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="bg-dark-hover/50 p-4 rounded-lg border border-dark-border">
              <div className="text-primary font-bold mb-2">📊 Dataset Híbrido</div>
              <div className="text-sm text-dark-muted">
                1.279 registros (76% SCF real + 24% sintético brasileiro)
              </div>
            </div>

            <div className="bg-dark-hover/50 p-4 rounded-lg border border-dark-border">
              <div className="text-success font-bold mb-2">⚡ Latência</div>
              <div className="text-sm text-dark-muted">
                Análise completa em 73ms (média)
              </div>
            </div>

            <div className="bg-dark-hover/50 p-4 rounded-lg border border-dark-border">
              <div className="text-warning font-bold mb-2">🎯 Validação</div>
              <div className="text-sm text-dark-muted">
                Validação cruzada 5-fold estratificada
              </div>
            </div>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
        >
          <Link to="/simulacao">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-premium w-full text-lg py-4"
            >
              📊 Ver Simulação
            </motion.button>
          </Link>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleNovaAnalise}
            className="bg-dark-card border-2 border-primary text-primary font-semibold px-6 py-4 rounded-xl hover:bg-primary hover:text-white transition-all duration-300 w-full text-lg"
          >
            🔄 Nova Análise
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.print()}
            className="bg-dark-card border-2 border-dark-border text-dark-text font-semibold px-6 py-4 rounded-xl hover:border-success transition-all duration-300 w-full text-lg"
          >
            🖨️ Imprimir
          </motion.button>

          <Link to="/">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-dark-card border-2 border-dark-border text-dark-text font-semibold px-6 py-4 rounded-xl hover:border-gradient-cyan transition-all duration-300 w-full text-lg"
            >
              🏠 Início
            </motion.button>
          </Link>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4 }}
          className="glass-card p-6 border-l-4 border-primary"
        >
          <p className="text-sm text-dark-muted text-center">
            <strong className="text-dark-text">Aviso Educacional:</strong> Este é um sistema desenvolvido para fins acadêmicos (TCC - Sistemas de Informação).
            As recomendações são baseadas em modelos de IA e não constituem aconselhamento financeiro profissional.
            Sempre consulte um assessor certificado antes de investir.
          </p>
        </motion.div>
      </div>
    </div>
  );
}
