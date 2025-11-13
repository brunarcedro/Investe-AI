import { motion } from 'framer-motion';
import { CSS3DCard } from '../components/Spline3D';

export default function Sobre() {
  const baseModels = [
    { nome: 'MLP 1', desc: 'Rede Neural (100,50)', acc: '88,3%', color: 'from-blue-500 to-blue-600' },
    { nome: 'MLP 2', desc: 'Rede Neural (50,25)', acc: '86,7%', color: 'from-cyan-500 to-cyan-600' },
    { nome: 'Random Forest', desc: '100 árvores de decisão', acc: '87,1%', color: 'from-green-500 to-green-600' },
    { nome: 'Gradient Boosting', desc: 'Boosting otimizado', acc: '88,9%', color: 'from-yellow-500 to-yellow-600' },
    { nome: 'XGBoost', desc: 'eXtreme Gradient Boosting', acc: '89,2%', color: 'from-orange-500 to-orange-600' },
    { nome: 'LightGBM', desc: 'Light Gradient Boosting', acc: '88,5%', color: 'from-purple-500 to-purple-600' },
    { nome: 'Extra Trees', desc: 'Extremely Randomized Trees', acc: '86,9%', color: 'from-pink-500 to-pink-600' },
  ];

  const metricsData = [
    { label: 'Acurácia', value: '91,5%', sublabel: 'IC 95%: [91,0%, 92,0%]', icon: '🎯', color: 'text-success' },
    { label: 'Latência', value: '73ms', sublabel: 'Tempo médio de resposta', icon: '⚡', color: 'text-primary' },
    { label: 'R² Score', value: '0,85', sublabel: 'Coeficiente de determinação', icon: '📊', color: 'text-warning' },
    { label: 'MAE', value: '2,78%', sublabel: 'Erro absoluto médio', icon: '📉', color: 'text-gradient-purple' },
  ];

  const assetClasses = [
    { icon: '💰', title: 'Renda Fixa', desc: 'Tesouro Direto, CDB, LCI/LCA', color: 'from-green-500 to-green-600' },
    { icon: '📈', title: 'Ações Brasil', desc: 'B3, ETFs, Ações individuais', color: 'from-blue-500 to-blue-600' },
    { icon: '🌎', title: 'Ações Internacional', desc: 'S&P 500, ETFs globais, BDRs', color: 'from-purple-500 to-purple-600' },
    { icon: '🏢', title: 'Fundos Imobiliários', desc: 'FIIs de tijolo, papel, logística', color: 'from-orange-500 to-orange-600' },
    { icon: '⚡', title: 'Commodities', desc: 'Ouro, petróleo, mineradoras', color: 'from-yellow-500 to-yellow-600' },
    { icon: '₿', title: 'Criptomoedas', desc: 'Bitcoin, Ethereum, ETFs cripto', color: 'from-pink-500 to-pink-600' },
  ];

  const techStack = {
    backend: [
      'Python 3.11+',
      'FastAPI (API REST)',
      'scikit-learn 1.3+',
      'pandas, numpy',
      'SMOTE, Grid Search',
      'Joblib (serialização)',
    ],
    frontend: [
      'React 18',
      'Vite',
      'TailwindCSS',
      'Framer Motion',
      'Recharts',
      'Axios',
    ],
    ml: [
      'MLPClassifier/Regressor',
      'XGBoost, LightGBM',
      'Random Forest',
      'Gradient Boosting',
      'Extra Trees',
      'Stacking Ensemble',
    ],
  };

  return (
    <div className="min-h-screen py-12 px-4">
      {/* Hero Section */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-gradient-purple to-gradient-cyan bg-clip-text text-transparent">
            Sobre o Investe-AI
          </h1>
          <p className="text-xl text-dark-muted max-w-3xl mx-auto">
            Sistema Inteligente de Recomendação de Investimentos baseado em
            <span className="text-primary font-semibold"> Arquitetura Dual de Redes Neurais</span> com
            <span className="text-success font-semibold"> Stacking Ensemble</span>
          </p>
        </motion.div>

        {/* Métricas Principais */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {metricsData.map((metric, idx) => (
            <div key={idx} className="glass-card p-6 text-center hover:scale-105 transition-transform duration-300">
              <div className="text-4xl mb-2">{metric.icon}</div>
              <div className={`text-3xl font-bold ${metric.color} mb-1`}>{metric.value}</div>
              <div className="text-sm font-semibold text-dark-text mb-1">{metric.label}</div>
              <div className="text-xs text-dark-muted">{metric.sublabel}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* TCC Section */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <CSS3DCard>
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <span>🎓</span> Trabalho de Conclusão de Curso
            </h2>
            <p className="text-dark-muted mb-6 leading-relaxed">
              Este sistema foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de
              <strong> Sistemas de Informação</strong> do IFES (Instituto Federal do Espírito Santo),
              representando a aplicação prática de técnicas avançadas de <strong>Machine Learning</strong> e
              <strong> Deep Learning</strong> para resolver um problema social relevante: a democratização
              do acesso à assessoria de investimentos para jovens brasileiros.
            </p>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-dark-hover/50 p-6 rounded-lg border border-dark-border">
                <p className="text-dark-muted mb-2"><strong className="text-dark-text">Desenvolvido por:</strong> Bruna Ribeiro Cedro</p>
                <p className="text-dark-muted mb-2"><strong className="text-dark-text">Instituição:</strong> IFES - Instituto Federal do Espírito Santo</p>
                <p className="text-dark-muted mb-2"><strong className="text-dark-text">Curso:</strong> Sistemas de Informação</p>
                <p className="text-dark-muted"><strong className="text-dark-text">Ano:</strong> 2025</p>
              </div>
              <div className="bg-gradient-to-br from-primary/10 to-gradient-purple/10 p-6 rounded-lg border border-primary/30">
                <p className="text-sm text-dark-muted mb-3">
                  <strong className="text-primary">Público-alvo:</strong> Jovens brasileiros de 18 a 25 anos
                </p>
                <p className="text-sm text-dark-muted mb-3">
                  <strong className="text-success">Objetivo:</strong> Democratizar acesso à assessoria financeira
                </p>
                <p className="text-sm text-dark-muted">
                  <strong className="text-warning">Conformidade:</strong> LGPD e Instrução CVM 539/2013
                </p>
              </div>
            </div>
          </CSS3DCard>
        </motion.div>
      </section>

      {/* Arquitetura Dual */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4">
            🧠 Arquitetura <span className="text-primary">Dual</span> de Redes Neurais
          </h2>
          <p className="text-xl text-dark-muted max-w-3xl mx-auto">
            O sistema utiliza duas redes neurais especializadas trabalhando em conjunto,
            conectadas em pipeline sequencial para máxima precisão
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* Primeira Rede Neural */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
          >
            <CSS3DCard className="h-full bg-gradient-to-br from-primary/5 to-gradient-cyan/5">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-2xl font-bold mb-4 text-primary">1ª Rede Neural</h3>
              <p className="text-dark-text font-semibold mb-4">Classificação de Perfil de Risco</p>

              <div className="space-y-3 mb-6">
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Entrada:</strong> 15 features do perfil do investidor
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Técnica:</strong> Stacking Ensemble com 7 modelos de ML
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Saída:</strong> Perfil de risco (Conservador/Moderado/Agressivo) + score 0-1
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Acurácia:</strong> 91,5% (IC 95%: [91,0%, 92,0%])
                  </span>
                </div>
              </div>

              <div className="bg-dark-hover/50 p-4 rounded-lg border border-dark-border">
                <p className="text-xs text-dark-muted">
                  <strong className="text-primary">Feature Engineering:</strong> 15 features originais expandidas para 26 através de
                  engenharia de características (patrimônio/renda, expertise_score, etc.)
                </p>
              </div>
            </CSS3DCard>
          </motion.div>

          {/* Segunda Rede Neural */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <CSS3DCard className="h-full bg-gradient-to-br from-success/5 to-gradient-cyan/5">
              <div className="text-5xl mb-4">💼</div>
              <h3 className="text-2xl font-bold mb-4 text-success">2ª Rede Neural</h3>
              <p className="text-dark-text font-semibold mb-4">Alocação Personalizada de Portfólio</p>

              <div className="space-y-3 mb-6">
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Entrada:</strong> Score de risco + contexto do investidor (8 features)
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Arquitetura:</strong> MLPRegressor (100, 50) com learning rate adaptativo
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Saída:</strong> Alocação percentual em 6 classes de ativos (soma = 100%)
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-dark-muted text-sm">
                    <strong className="text-dark-text">Performance:</strong> R²=0,85 | MAE=2,78% | RMSE=3,51%
                  </span>
                </div>
              </div>

              <div className="bg-dark-hover/50 p-4 rounded-lg border border-dark-border">
                <p className="text-xs text-dark-muted">
                  <strong className="text-success">Otimização:</strong> Grid Search com 426 combinações de hiperparâmetros
                  testadas em 10h 33min de treinamento
                </p>
              </div>
            </CSS3DCard>
          </motion.div>
        </div>

        {/* Stacking Ensemble Visualization */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <CSS3DCard>
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <span>🏆</span> Stacking Ensemble com 7 Modelos Base
            </h3>
            <p className="text-dark-muted mb-6">
              A primeira rede neural utiliza <strong className="text-primary">Stacking Ensemble</strong>,
              técnica avançada de ensemble learning que combina predições de 7 modelos heterogêneos
              através de um meta-modelo (Logistic Regression), alcançando performance superior à
              qualquer modelo individual.
            </p>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              {baseModels.map((model, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.05 }}
                  className="bg-dark-hover/50 p-4 rounded-lg border-l-4 border-primary hover:scale-105 transition-transform duration-300"
                  style={{ borderLeftColor: `var(--gradient-${model.color.split('-')[1]})` }}
                >
                  <div className="text-2xl font-bold text-primary mb-1">{model.acc}</div>
                  <div className="text-sm font-bold text-dark-text mb-1">{model.nome}</div>
                  <div className="text-xs text-dark-muted">{model.desc}</div>
                </motion.div>
              ))}

              {/* Meta-Modelo */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 0.4 }}
                className="bg-gradient-to-br from-success/20 to-primary/20 p-4 rounded-lg border-2 border-success"
              >
                <div className="text-3xl font-bold text-success mb-1">91,5%</div>
                <div className="text-sm font-bold text-dark-text mb-1">🏆 Stacking</div>
                <div className="text-xs text-dark-muted mb-2">Meta-modelo final</div>
                <div className="text-[10px] text-success">IC 95%: [91,0%, 92,0%]</div>
              </motion.div>
            </div>

            <div className="bg-gradient-to-r from-primary/10 to-success/10 p-6 rounded-lg border border-primary/30">
              <p className="text-sm text-dark-muted">
                <strong className="text-primary">🔍 Superioridade Comprovada:</strong> O Stacking alcançou 91,5% de acurácia,
                superando o melhor modelo base individual (XGBoost: 89,2%) em <strong>+2,3 pontos percentuais</strong> e
                o melhor trabalho correlato brasileiro em <strong>+7,8 pontos percentuais</strong> (Martins & Costa, 2023: 83,7%).
              </p>
            </div>
          </CSS3DCard>
        </motion.div>
      </section>

      {/* Dataset e Metodologia */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4">
            📊 Dataset <span className="text-primary">Híbrido</span> e Metodologia
          </h2>
          <p className="text-xl text-dark-muted max-w-3xl mx-auto">
            Combinação inédita de dados reais internacionais com dados sintéticos brasileiros,
            validados por especialista certificado
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
          >
            <CSS3DCard className="h-full">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-bold mb-3 text-primary">Composição do Dataset</h3>
              <ul className="space-y-3 text-sm text-dark-muted">
                <li className="flex items-start gap-2">
                  <span className="text-success font-bold">76%</span>
                  <span>Dados reais do <strong>Survey of Consumer Finances (SCF)</strong> do Federal Reserve Board (USA)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-warning font-bold">24%</span>
                  <span>Dados sintéticos adaptados ao contexto brasileiro (faixas de renda, cultura financeira)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">1.279</span>
                  <span>Registros totais após limpeza e balanceamento via SMOTE</span>
                </li>
              </ul>
            </CSS3DCard>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <CSS3DCard className="h-full">
              <div className="text-4xl mb-4">🔬</div>
              <h3 className="text-xl font-bold mb-3 text-success">Validação Rigorosa</h3>
              <ul className="space-y-3 text-sm text-dark-muted">
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Validação cruzada estratificada 5-fold</strong> com distribuição balanceada de classes</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Grid Search</strong> com 426 combinações de hiperparâmetros (10h 33min)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Intervalo de confiança 95%</strong> calculado via distribuição t-Student</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Seeds fixos</strong> (random_state=42) para reprodutibilidade total</span>
                </li>
              </ul>
            </CSS3DCard>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
          >
            <CSS3DCard className="h-full">
              <div className="text-4xl mb-4">⚙️</div>
              <h3 className="text-xl font-bold mb-3 text-warning">Feature Engineering</h3>
              <ul className="space-y-3 text-sm text-dark-muted">
                <li className="flex items-start gap-2">
                  <span className="text-warning font-bold">15→26</span>
                  <span>Features expandidas através de engenharia de características</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span>Features derivadas: <strong>patrimonio_sobre_renda, expertise_score, tolerancia_diff</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Normalização Z-score</strong> para features numéricas</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Label Encoding</strong> para variáveis categóricas ordinais</span>
                </li>
              </ul>
            </CSS3DCard>
          </motion.div>
        </div>
      </section>

      {/* Classes de Ativos */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4">
            🎯 6 Classes de <span className="text-primary">Ativos</span>
          </h2>
          <p className="text-xl text-dark-muted max-w-3xl mx-auto">
            Portfólio diversificado cobrindo todas as principais categorias de investimento
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {assetClasses.map((asset, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.08 }}
            >
              <CSS3DCard className="text-center hover:scale-105 transition-transform duration-300">
                <div className="text-5xl mb-4">{asset.icon}</div>
                <h3 className="text-xl font-bold mb-2 text-dark-text">{asset.title}</h3>
                <p className="text-sm text-dark-muted">{asset.desc}</p>
                <div className={`h-1 w-20 mx-auto mt-4 rounded-full bg-gradient-to-r ${asset.color}`} />
              </CSS3DCard>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Stack Tecnológica */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4">
            💻 Stack <span className="text-primary">Tecnológica</span>
          </h2>
          <p className="text-xl text-dark-muted max-w-3xl mx-auto">
            Tecnologias modernas e escaláveis para máximo desempenho
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <CSS3DCard className="h-full">
              <h3 className="text-xl font-bold mb-4 text-primary flex items-center gap-2">
                <span>🐍</span> Backend
              </h3>
              <ul className="space-y-2">
                {techStack.backend.map((tech, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-dark-muted">
                    <span className="text-success">✓</span>
                    <span>{tech}</span>
                  </li>
                ))}
              </ul>
            </CSS3DCard>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
          >
            <CSS3DCard className="h-full">
              <h3 className="text-xl font-bold mb-4 text-success flex items-center gap-2">
                <span>⚛️</span> Frontend
              </h3>
              <ul className="space-y-2">
                {techStack.frontend.map((tech, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-dark-muted">
                    <span className="text-success">✓</span>
                    <span>{tech}</span>
                  </li>
                ))}
              </ul>
            </CSS3DCard>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <CSS3DCard className="h-full">
              <h3 className="text-xl font-bold mb-4 text-warning flex items-center gap-2">
                <span>🤖</span> Machine Learning
              </h3>
              <ul className="space-y-2">
                {techStack.ml.map((tech, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-dark-muted">
                    <span className="text-success">✓</span>
                    <span>{tech}</span>
                  </li>
                ))}
              </ul>
            </CSS3DCard>
          </motion.div>
        </div>
      </section>

      {/* Conformidade Regulatória */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <CSS3DCard className="bg-gradient-to-br from-primary/5 to-success/5">
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <span>🔒</span> Conformidade Regulatória
            </h2>

            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div className="bg-dark-hover/50 p-6 rounded-lg border border-primary/30">
                <h3 className="text-xl font-bold text-primary mb-3">LGPD</h3>
                <p className="text-sm text-dark-muted mb-3">
                  Sistema em conformidade com a <strong>Lei Geral de Proteção de Dados (Lei 13.709/2018)</strong>:
                </p>
                <ul className="space-y-2 text-xs text-dark-muted">
                  <li className="flex items-start gap-2">
                    <span className="text-success">✓</span>
                    <span>Não há coleta de dados pessoais identificáveis</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-success">✓</span>
                    <span>Análise realizada sem armazenamento permanente</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-success">✓</span>
                    <span>Transparência na coleta e uso de informações</span>
                  </li>
                </ul>
              </div>

              <div className="bg-dark-hover/50 p-6 rounded-lg border border-success/30">
                <h3 className="text-xl font-bold text-success mb-3">CVM 539/2013</h3>
                <p className="text-sm text-dark-muted mb-3">
                  Alinhamento com a <strong>Instrução CVM 539/2013</strong> sobre adequação de produtos:
                </p>
                <ul className="space-y-2 text-xs text-dark-muted">
                  <li className="flex items-start gap-2">
                    <span className="text-success">✓</span>
                    <span>Análise de perfil de risco (suitability)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-success">✓</span>
                    <span>Alertas para casos de baixa confiança (&lt;60%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-success">✓</span>
                    <span>Recomendação de consulta com assessor certificado</span>
                  </li>
                </ul>
              </div>
            </div>

            <div className="bg-warning/10 border border-warning/30 p-6 rounded-lg">
              <p className="text-sm text-dark-muted">
                <strong className="text-warning">⚠️ Aviso Educacional:</strong> Este é um sistema desenvolvido para fins
                acadêmicos (TCC - Sistemas de Informação). As recomendações são baseadas em modelos de IA e não constituem
                aconselhamento financeiro profissional. Sempre consulte um assessor certificado (CFP®, CGA, AAI) antes de
                tomar decisões de investimento.
              </p>
            </div>
          </CSS3DCard>
        </motion.div>
      </section>

      {/* Comparação com Literatura */}
      <section className="container mx-auto max-w-7xl mb-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <CSS3DCard>
            <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
              <span>📈</span> Comparação com Trabalhos Correlatos
            </h2>

            <p className="text-dark-muted mb-6">
              O Investe-AI alcançou <strong className="text-success">91,5% de acurácia</strong>, superando
              significativamente trabalhos anteriores na literatura nacional e internacional:
            </p>

            <div className="space-y-4">
              <div className="bg-success/10 border-l-4 border-success p-4 rounded-r-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-dark-text">🏆 Investe-AI (2025)</span>
                  <span className="text-2xl font-bold text-success">91,5%</span>
                </div>
                <p className="text-xs text-dark-muted">Stacking Ensemble (7 modelos) | Dataset híbrido 1.279 registros | Brasil</p>
              </div>

              <div className="bg-dark-hover/50 border-l-4 border-primary p-4 rounded-r-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-dark-text">Martins & Costa (2023)</span>
                  <span className="text-xl font-bold text-primary">83,7%</span>
                </div>
                <p className="text-xs text-dark-muted">Random Forest | Dataset próprio | Brasil</p>
                <p className="text-xs text-warning mt-1"><strong>+7,8 pp</strong> de vantagem do Investe-AI</p>
              </div>

              <div className="bg-dark-hover/50 border-l-4 border-dark-border p-4 rounded-r-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-dark-text">Baseline Sintético</span>
                  <span className="text-xl font-bold text-dark-muted">46,7%</span>
                </div>
                <p className="text-xs text-dark-muted">Classificação aleatória | 3 classes balanceadas</p>
                <p className="text-xs text-warning mt-1"><strong>+44,8 pp</strong> de ganho absoluto</p>
              </div>
            </div>

            <div className="mt-6 bg-gradient-to-r from-primary/10 to-success/10 p-6 rounded-lg border border-primary/30">
              <p className="text-sm text-dark-muted">
                <strong className="text-primary">🎓 Contribuição Científica:</strong> Este trabalho representa o
                estado da arte em sistemas brasileiros de recomendação de investimentos baseados em ML, sendo o
                primeiro a utilizar Stacking Ensemble com 7 modelos heterogêneos e dataset híbrido validado
                (SCF + sintético brasileiro).
              </p>
            </div>
          </CSS3DCard>
        </motion.div>
      </section>

      {/* CTA Final */}
      <section className="container mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="glass-card p-12 text-center relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-gradient-purple/5 to-gradient-cyan/10" />

          <div className="relative z-10">
            <h2 className="text-4xl font-bold mb-4">Experimente o Sistema</h2>
            <p className="text-xl text-dark-muted mb-8 max-w-2xl mx-auto">
              Descubra seu perfil de investidor e receba uma carteira personalizada
              analisada por 7 modelos de Machine Learning
            </p>

            <a href="/questionario">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-premium text-xl px-12 py-5"
              >
                🚀 Começar Análise Gratuita
              </motion.button>
            </a>

            <p className="text-sm text-dark-muted mt-6">
              ✓ Gratuito • ✓ Sem cadastro • ✓ Resultados em 73ms
            </p>
          </div>
        </motion.div>
      </section>
    </div>
  );
}
