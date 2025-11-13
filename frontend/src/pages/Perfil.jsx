import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { recomendarPortfolio } from '../services/api';
import Loading from '../components/Loading';

export default function Perfil() {
  const navigate = useNavigate();
  const [perfilData, setPerfilData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [xp, setXp] = useState(0);
  const [showConfetti, setShowConfetti] = useState(false);

  useEffect(() => {
    // Carregar dados do perfil do localStorage
    const data = localStorage.getItem('perfil_investidor');
    if (data) {
      setPerfilData(JSON.parse(data));
      // Show confetti animation on mount
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    } else {
      navigate('/questionario');
    }

    // Carregar XP conquistado
    const xpConquistado = localStorage.getItem('xp_conquistado');
    if (xpConquistado) {
      setXp(parseInt(xpConquistado));
    }
  }, [navigate]);

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="text-6xl mb-6 animate-spin">🧠</div>
          <p className="text-xl text-dark-text">Gerando sua carteira personalizada...</p>
          <p className="text-dark-muted mt-2">Analisando mercado com IA</p>
        </motion.div>
      </div>
    );
  }

  if (!perfilData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⏳</div>
          <p className="text-dark-text">Carregando seu perfil...</p>
        </div>
      </div>
    );
  }

  // Determinar estilo baseado no perfil (dark theme)
  const getPerfilStyle = (perfil) => {
    if (perfil.includes('Conservador')) {
      return {
        color: 'text-blue-400',
        gradient: 'from-blue-500 to-cyan-500',
        icon: '🛡️',
        glow: 'shadow-glow',
        badge: 'bg-blue-500/20 border-blue-500/50',
      };
    } else if (perfil.includes('Moderado')) {
      return {
        color: 'text-warning',
        gradient: 'from-warning to-orange-500',
        icon: '⚖️',
        glow: 'shadow-glow-warning',
        badge: 'bg-warning/20 border-warning/50',
      };
    } else if (perfil.includes('Arrojado')) {
      return {
        color: 'text-danger',
        gradient: 'from-danger to-pink-500',
        icon: '🚀',
        glow: 'shadow-glow-danger',
        badge: 'bg-danger/20 border-danger/50',
      };
    }
    return {
      color: 'text-primary',
      gradient: 'from-primary to-gradient-cyan',
      icon: '📊',
      glow: 'shadow-glow',
      badge: 'bg-primary/20 border-primary/50',
    };
  };

  const style = getPerfilStyle(perfilData.perfil);

  // Descrições detalhadas por perfil (mantendo conteúdo)
  const descricoesPerfil = {
    'Muito Conservador': {
      resumo: 'Você prioriza a segurança absoluta do seu capital',
      caracteristicas: [
        'Não aceita perder dinheiro em nenhuma hipótese',
        'Prefere rendimentos baixos mas garantidos',
        'Valoriza liquidez e disponibilidade imediata',
        'Ideal para reserva de emergência'
      ],
      investimentos: [
        'Tesouro Selic',
        'Poupança',
        'CDB com liquidez diária',
        'Fundos DI'
      ],
      retornoEsperado: '100% - 110% do CDI/ano',
      riscoEsperado: 'Muito Baixo',
      volatilidade: 15,
      liquidez: 95,
      rentabilidade: 40,
    },
    'Conservador': {
      resumo: 'Você busca segurança com pequena exposição a riscos controlados',
      caracteristicas: [
        'Aceita pequenas variações no capital',
        'Prefere renda fixa com bons rendimentos',
        'Tolera pouca volatilidade',
        'Horizonte de curto a médio prazo'
      ],
      investimentos: [
        'Tesouro IPCA+',
        'CDBs de bancos médios (110-120% CDI)',
        'LCI/LCA',
        'Debêntures de baixo risco'
      ],
      retornoEsperado: '110% - 130% do CDI/ano',
      riscoEsperado: 'Baixo',
      volatilidade: 30,
      liquidez: 75,
      rentabilidade: 55,
    },
    'Moderado': {
      resumo: 'Você equilibra segurança e busca por crescimento',
      caracteristicas: [
        'Aceita volatilidade moderada',
        'Busca diversificação entre renda fixa e variável',
        'Tolera perdas temporárias por ganhos maiores',
        'Horizonte de médio a longo prazo'
      ],
      investimentos: [
        'Mix de Tesouro Direto e ações',
        'Fundos multimercado',
        'ETFs de índices',
        'Fundos imobiliários',
        'Até 30-40% em renda variável'
      ],
      retornoEsperado: '12% - 18% ao ano',
      riscoEsperado: 'Médio',
      volatilidade: 55,
      liquidez: 60,
      rentabilidade: 70,
    },
    'Arrojado': {
      resumo: 'Você aceita riscos maiores em busca de retornos superiores',
      caracteristicas: [
        'Tolera alta volatilidade',
        'Foco em crescimento de longo prazo',
        'Aceita perdas de curto prazo',
        'Conhecimento intermediário/avançado do mercado'
      ],
      investimentos: [
        'Ações individuais',
        'ETFs internacionais',
        'Fundos de ações',
        'Small caps',
        'Até 60-70% em renda variável'
      ],
      retornoEsperado: '18% - 25%+ ao ano',
      riscoEsperado: 'Alto',
      volatilidade: 80,
      liquidez: 50,
      rentabilidade: 85,
    },
    'Muito Arrojado': {
      resumo: 'Você busca maximizar retornos aceitando alta volatilidade',
      caracteristicas: [
        'Tolera perdas significativas de curto prazo',
        'Foco exclusivo em crescimento máximo',
        'Conhecimento avançado do mercado',
        'Horizonte de muito longo prazo (10+ anos)'
      ],
      investimentos: [
        'Ações de crescimento (growth)',
        'Small caps e micro caps',
        'Criptomoedas (pequena parcela)',
        'Ações internacionais',
        'Derivativos (experientes)',
        'Até 80-100% em renda variável'
      ],
      retornoEsperado: '25%+ ao ano (variável)',
      riscoEsperado: 'Muito Alto',
      volatilidade: 95,
      liquidez: 35,
      rentabilidade: 95,
    }
  };

  const detalhes = descricoesPerfil[perfilData.perfil] || descricoesPerfil['Moderado'];

  const handleContinuar = async () => {
    setLoading(true);

    try {
      const dadosFormulario = localStorage.getItem('dados_formulario');
      if (!dadosFormulario) {
        navigate('/questionario');
        return;
      }

      const dados = JSON.parse(dadosFormulario);
      const resultado = await recomendarPortfolio(dados);
      localStorage.setItem('resultado_investimento', JSON.stringify(resultado));

      // Add XP bonus for viewing portfolio
      const novoXp = xp + 30;
      setXp(novoXp);
      localStorage.setItem('xp_conquistado', novoXp);

      navigate('/resultado');
    } catch (error) {
      console.error('Erro ao gerar recomendação:', error);
      setLoading(false);
      alert('Erro ao gerar recomendação. Tente novamente.');
    }
  };

  // Calculate investor level based on XP
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
        {/* Confetti Effect */}
        <AnimatePresence>
          {showConfetti && (
            <motion.div
              initial={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 pointer-events-none z-50"
            >
              {[...Array(30)].map((_, i) => (
                <motion.div
                  key={i}
                  initial={{ y: -100, x: Math.random() * window.innerWidth, opacity: 1 }}
                  animate={{
                    y: window.innerHeight + 100,
                    rotate: Math.random() * 360,
                    opacity: 0
                  }}
                  transition={{ duration: 2 + Math.random() * 2, ease: 'linear' }}
                  className={`absolute w-3 h-3 rounded-full ${
                    i % 3 === 0 ? 'bg-primary' : i % 3 === 1 ? 'bg-success' : 'bg-warning'
                  }`}
                />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Header com XP Badge */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-between items-center mb-8"
        >
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-dark-text mb-2">
              Seu Perfil de Investidor
            </h1>
            <p className="text-dark-muted">Análise completa do seu perfil de risco</p>
          </div>

          {/* XP Badge */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="glass-card px-6 py-4 text-center"
          >
            <div className="text-3xl mb-1">{nivel.icon}</div>
            <div className={`text-sm font-bold ${nivel.color}`}>{nivel.nome}</div>
            <div className="text-2xl font-bold text-primary">{xp} XP</div>
          </motion.div>
        </motion.div>

        {/* Hero Card - Perfil Principal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="relative overflow-hidden rounded-2xl mb-8"
        >
          {/* Gradient Background */}
          <div className={`absolute inset-0 bg-gradient-to-br ${style.gradient} opacity-20`} />

          <div className="relative glass-card p-8 md:p-12">
            <div className="flex flex-col md:flex-row items-center gap-8">
              {/* Icon */}
              <motion.div
                animate={{
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  repeatType: "reverse"
                }}
                className={`text-8xl ${style.glow}`}
              >
                {style.icon}
              </motion.div>

              {/* Content */}
              <div className="flex-1 text-center md:text-left">
                <div className={`inline-block px-4 py-2 ${style.badge} border rounded-full mb-4`}>
                  <span className="text-sm font-bold text-dark-text">PERFIL IDENTIFICADO</span>
                </div>

                <h2 className={`text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r ${style.gradient} bg-clip-text text-transparent`}>
                  {perfilData.perfil}
                </h2>

                <p className="text-xl text-dark-muted mb-4">
                  {detalhes.resumo}
                </p>

                {/* Score de Risco */}
                <div className="flex items-center justify-center md:justify-start gap-4">
                  <div className="text-dark-muted">Score de Risco:</div>
                  <div className="relative w-32 h-4 bg-dark-hover rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${perfilData.score_risco * 100}%` }}
                      transition={{ duration: 1, delay: 0.5 }}
                      className={`h-full bg-gradient-to-r ${style.gradient}`}
                    />
                  </div>
                  <div className={`text-2xl font-bold ${style.color}`}>
                    {(perfilData.score_risco * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Stats Grid - Métricas Visuais */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          {/* Volatilidade */}
          <div className="card-hover group">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-dark-muted text-sm mb-1 flex items-center">
                  Volatilidade
                  <Tooltip text="Medida de variação dos preços. Alta volatilidade = mais risco, mas também mais oportunidades." />
                </div>
                <div className="text-3xl font-bold text-danger">{detalhes.volatilidade}%</div>
              </div>
              <div className="text-4xl group-hover:scale-110 transition-transform">📈</div>
            </div>
            <div className="w-full h-2 bg-dark-hover rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                whileInView={{ width: `${detalhes.volatilidade}%` }}
                viewport={{ once: true }}
                transition={{ duration: 1 }}
                className="h-full bg-gradient-to-r from-danger to-pink-500"
              />
            </div>
          </div>

          {/* Liquidez */}
          <div className="card-hover group">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-dark-muted text-sm mb-1 flex items-center">
                  Liquidez
                  <Tooltip text="Facilidade de converter investimentos em dinheiro rapidamente sem perder valor." />
                </div>
                <div className="text-3xl font-bold text-primary">{detalhes.liquidez}%</div>
              </div>
              <div className="text-4xl group-hover:scale-110 transition-transform">💧</div>
            </div>
            <div className="w-full h-2 bg-dark-hover rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                whileInView={{ width: `${detalhes.liquidez}%` }}
                viewport={{ once: true }}
                transition={{ duration: 1, delay: 0.2 }}
                className="h-full bg-gradient-to-r from-primary to-gradient-cyan"
              />
            </div>
          </div>

          {/* Rentabilidade Esperada */}
          <div className="card-hover group">
            <div className="flex items-start justify-between mb-4">
              <div>
                <div className="text-dark-muted text-sm mb-1 flex items-center">
                  Rentabilidade Esperada
                  <Tooltip text="Potencial de retorno financeiro baseado no perfil de risco. Maior rentabilidade geralmente implica maior risco." />
                </div>
                <div className="text-3xl font-bold text-success">{detalhes.rentabilidade}%</div>
              </div>
              <div className="text-4xl group-hover:scale-110 transition-transform">💰</div>
            </div>
            <div className="w-full h-2 bg-dark-hover rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                whileInView={{ width: `${detalhes.rentabilidade}%` }}
                viewport={{ once: true }}
                transition={{ duration: 1, delay: 0.4 }}
                className="h-full bg-gradient-to-r from-success to-green-600"
              />
            </div>
          </div>
        </motion.div>

        {/* Características e Investimentos - 2 Colunas */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Características do Perfil */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="card-hover"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">✨</div>
              <h3 className="text-2xl font-bold text-dark-text">Características</h3>
            </div>
            <ul className="space-y-3">
              {detalhes.caracteristicas.map((caract, idx) => (
                <motion.li
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + idx * 0.1 }}
                  className="flex items-start gap-3"
                >
                  <span className="text-success text-xl mt-1 flex-shrink-0">✓</span>
                  <span className="text-dark-muted">{caract}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          {/* Investimentos Típicos */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            className="card-hover"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">📊</div>
              <h3 className="text-2xl font-bold text-dark-text">Investimentos Típicos</h3>
            </div>
            <div className="space-y-3">
              {detalhes.investimentos.map((inv, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.7 + idx * 0.1 }}
                  className="flex items-center gap-3 bg-dark-hover rounded-lg p-3 hover:bg-dark-border transition-colors"
                >
                  <span className={`${style.color} text-xl flex-shrink-0`}>→</span>
                  <span className="text-dark-text font-medium">{inv}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Suas Características Pessoais */}
        {perfilData.caracteristicas && perfilData.caracteristicas.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="glass-card p-8 mb-8"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-4xl">👤</div>
              <h3 className="text-2xl font-bold text-dark-text">Sobre Você</h3>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {perfilData.caracteristicas.map((caract, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9 + idx * 0.1 }}
                  className="flex items-start gap-3"
                >
                  <span className="text-primary text-xl flex-shrink-0">•</span>
                  <span className="text-dark-muted">{caract}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Expectativas - Cards */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="grid md:grid-cols-2 gap-6 mb-8"
        >
          {/* Retorno Esperado */}
          <div className="card-hover border-l-4 border-success">
            <div className="flex items-start gap-4">
              <div className="text-5xl">💵</div>
              <div className="flex-1">
                <div className="text-dark-muted text-sm mb-2 flex items-center">
                  RETORNO ESPERADO ANUAL
                  <Tooltip text="Ganho percentual médio esperado por ano, considerando histórico do mercado para esse perfil." />
                </div>
                <div className="text-3xl font-bold text-success mb-2">{detalhes.retornoEsperado}</div>
                <div className="text-sm text-dark-muted">
                  Baseado em histórico de mercado
                </div>
              </div>
            </div>
          </div>

          {/* Nível de Risco */}
          <div className="card-hover border-l-4 border-warning">
            <div className="flex items-start gap-4">
              <div className="text-5xl">⚠️</div>
              <div className="flex-1">
                <div className="text-dark-muted text-sm mb-2 flex items-center">
                  NÍVEL DE RISCO
                  <Tooltip text="Classificação do risco baseado na volatilidade esperada dos investimentos recomendados." />
                </div>
                <div className="text-3xl font-bold text-warning mb-2">{detalhes.riscoEsperado}</div>
                <div className="text-sm text-dark-muted">
                  {perfilData.descricao || 'Perfil analisado por IA'}
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* CTA Final */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 1.2 }}
          className="relative overflow-hidden rounded-2xl"
        >
          {/* Gradient Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-gradient-purple/10 to-gradient-cyan/20" />

          <div className="relative glass-card p-12 text-center">
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-6xl mb-6"
            >
              🎯
            </motion.div>

            <h2 className="text-4xl font-bold mb-4 text-dark-text">
              Pronto para ver sua carteira personalizada?
            </h2>

            <p className="text-xl text-dark-muted mb-8 max-w-2xl mx-auto">
              Agora que você conhece seu perfil <span className={`font-bold ${style.color}`}>{perfilData.perfil}</span>,
              vamos montar uma carteira ideal para você com base em dados reais do mercado!
            </p>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleContinuar}
              className="btn-premium text-xl px-12 py-5"
            >
              💼 Ver Minha Carteira Recomendada
            </motion.button>

            <p className="text-sm text-dark-muted mt-6">
              ✓ Alocação baseada em IA • ✓ Produtos reais • ✓ +30 XP ao visualizar
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
