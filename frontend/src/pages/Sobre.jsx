import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function Sobre() {
  const navigate = useNavigate();

  const baseModels = [
    { nome: 'MLP 1', desc: 'Rede Neural (100,50)', acc: '88,3%' },
    { nome: 'MLP 2', desc: 'Rede Neural (50,25)', acc: '86,7%' },
    { nome: 'Random Forest', desc: '100 árvores de decisão', acc: '87,1%' },
    { nome: 'Gradient Boosting', desc: 'Boosting otimizado', acc: '88,9%' },
    { nome: 'XGBoost', desc: 'eXtreme Gradient Boosting', acc: '89,2%' },
    { nome: 'LightGBM', desc: 'Light Gradient Boosting', acc: '88,5%' },
    { nome: 'Extra Trees', desc: 'Extremely Randomized Trees', acc: '86,9%' },
  ];

  const metricsData = [
    { label: 'Acurácia', value: '88,2%', sublabel: 'Voting Classifier' },
    { label: 'Latência', value: '<100ms', sublabel: 'Tempo médio' },
    { label: 'R² Score', value: '0,82', sublabel: 'Ensemble V4' },
    { label: 'Perfis', value: '3', sublabel: 'Classes de risco' },
  ];

  const assetClasses = [
    { title: 'Renda Fixa', desc: 'Tesouro Direto, CDB, LCI/LCA' },
    { title: 'Ações Brasil', desc: 'B3, ETFs, Ações individuais' },
    { title: 'Ações Internacional', desc: 'S&P 500, ETFs globais, BDRs' },
    { title: 'Fundos Imobiliários', desc: 'FIIs de tijolo, papel, logística' },
    { title: 'Commodities', desc: 'Ouro, petróleo, mineradoras' },
    { title: 'Criptomoedas', desc: 'Bitcoin, Ethereum, ETFs cripto' },
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
    <div className="min-h-screen bg-academic-bg">
      {/* Header */}
      <header className="border-b border-academic-border bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-primary">Investe-AI</h1>
            </Link>
            <nav className="flex gap-6">
              <Link to="/" className="text-academic-text-secondary hover:text-primary transition-colors font-medium">
                Início
              </Link>
              <Link to="/questionario" className="text-academic-text-secondary hover:text-primary transition-colors font-medium">
                Análise
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="inline-block mb-4 px-4 py-2 bg-primary-50 rounded-full">
            <span className="text-primary font-semibold text-sm">Trabalho de Conclusão de Curso • IFES</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-academic-text mb-6">
            Sistema Inteligente de Recomendação de Investimentos
          </h1>
          <p className="text-xl text-academic-text-secondary max-w-3xl mx-auto">
            Arquitetura Dual de Redes Neurais com Stacking Ensemble para classificação
            de perfil de risco e alocação personalizada de portfólio
          </p>
        </motion.div>

        {/* Métricas Principais */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16"
        >
          {metricsData.map((metric, idx) => (
            <div key={idx} className="card-academic p-6 text-center">
              <div className="text-4xl font-bold text-primary mb-2">{metric.value}</div>
              <div className="text-sm font-medium text-academic-text mb-1">{metric.label}</div>
              <div className="text-xs text-academic-text-muted">{metric.sublabel}</div>
            </div>
          ))}
        </motion.div>

        {/* TCC Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card-academic p-8 mb-16"
        >
          <h2 className="text-3xl font-bold text-academic-text mb-6">
            Trabalho de Conclusão de Curso
          </h2>
          <p className="text-academic-text-secondary mb-6 leading-relaxed">
            Este sistema foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de
            <strong> Sistemas de Informação</strong> do IFES (Instituto Federal do Espírito Santo),
            representando a aplicação prática de técnicas avançadas de <strong>Machine Learning</strong> e
            <strong> Deep Learning</strong> para resolver um problema social relevante: a democratização
            do acesso à assessoria de investimentos.
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-academic-bg-secondary p-6 rounded-lg border border-academic-border">
              <p className="text-academic-text-secondary mb-2"><strong className="text-academic-text">Desenvolvido por:</strong> Bruna Ribeiro Cedro</p>
              <p className="text-academic-text-secondary mb-2"><strong className="text-academic-text">Instituição:</strong> IFES - Instituto Federal do Espírito Santo</p>
              <p className="text-academic-text-secondary mb-2"><strong className="text-academic-text">Curso:</strong> Sistemas de Informação</p>
              <p className="text-academic-text-secondary"><strong className="text-academic-text">Ano:</strong> 2025</p>
            </div>
            <div className="bg-primary-50 p-6 rounded-lg border border-primary">
              <p className="text-sm text-academic-text-secondary mb-3">
                <strong className="text-primary">Público-alvo:</strong> Jovens brasileiros de 18 a 25 anos
              </p>
              <p className="text-sm text-academic-text-secondary mb-3">
                <strong className="text-primary">Objetivo:</strong> Democratizar acesso à assessoria financeira
              </p>
              <p className="text-sm text-academic-text-secondary">
                <strong className="text-primary">Conformidade:</strong> LGPD e Instrução CVM 539/2013
              </p>
            </div>
          </div>
        </motion.div>

        {/* Arquitetura Dual */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-academic-text mb-4">
              Arquitetura Dual de Redes Neurais
            </h2>
            <p className="text-xl text-academic-text-secondary max-w-3xl mx-auto">
              Duas redes neurais especializadas trabalhando em conjunto em pipeline sequencial
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Primeira Rede Neural */}
            <div className="card-academic p-8">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-2xl font-bold mb-4 text-primary">1ª Rede Neural</h3>
              <p className="font-semibold text-academic-text mb-4">Classificação de Perfil de Risco</p>

              <div className="space-y-3 mb-6">
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Entrada:</strong> 15 features do perfil do investidor
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Técnica:</strong> Voting Classifier (RF + MLP + SVM)
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Saída:</strong> 3 perfis de risco + probabilidades
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Acurácia:</strong> 88,2% (Soft Voting)
                  </span>
                </div>
              </div>

              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border">
                <p className="text-xs text-academic-text-secondary">
                  <strong className="text-primary">Ensemble:</strong> Random Forest (peso 0.4) + MLP(15,10,5) (peso 0.6) + SVM (arbitrador)
                </p>
              </div>
            </div>

            {/* Segunda Rede Neural */}
            <div className="card-academic p-8">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-2xl font-bold mb-4 text-primary">2ª Rede Neural</h3>
              <p className="font-semibold text-academic-text mb-4">Alocação Personalizada de Portfólio</p>

              <div className="space-y-3 mb-6">
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Entrada:</strong> 8 features base → 27 features (eng. agressivo)
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Arquitetura:</strong> Ensemble V4 (5 modelos heterogêneos)
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Saída:</strong> 6 classes de ativos (soma = 100%)
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-success font-bold">✓</span>
                  <span className="text-academic-text-secondary text-sm">
                    <strong className="text-academic-text">Performance:</strong> R²=0,82 (melhoria de +25.82pp)
                  </span>
                </div>
              </div>

              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border">
                <p className="text-xs text-academic-text-secondary">
                  <strong className="text-primary">Modelos:</strong> 2 MLPs + Random Forest + Gradient Boosting + Extra Trees com pesos dinâmicos
                </p>
              </div>
            </div>
          </div>

          {/* Voting Classifier Info */}
          <div className="card-academic p-8">
            <h3 className="text-2xl font-bold mb-6 text-academic-text">
              Voting Classifier com Soft Voting
            </h3>
            <p className="text-academic-text-secondary mb-6">
              A primeira rede neural utiliza <strong className="text-primary">Voting Classifier</strong>,
              técnica de ensemble learning que combina predições de 3 modelos heterogêneos
              (Random Forest, MLP e SVM) através de soft voting ponderado.
            </p>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border text-center">
                <div className="text-2xl font-bold text-primary mb-1">Random Forest</div>
                <div className="text-sm text-academic-text mb-1">300 árvores</div>
                <div className="text-xs text-academic-text-muted">Peso: 0.4</div>
              </div>

              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border text-center">
                <div className="text-2xl font-bold text-primary mb-1">MLP</div>
                <div className="text-sm text-academic-text mb-1">(256, 128, 64)</div>
                <div className="text-xs text-academic-text-muted">Peso: 0.6</div>
              </div>

              <div className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border text-center">
                <div className="text-2xl font-bold text-primary mb-1">SVM</div>
                <div className="text-sm text-academic-text mb-1">Kernel RBF</div>
                <div className="text-xs text-academic-text-muted">Arbitrador</div>
              </div>
            </div>

            <div className="bg-primary-50 p-6 rounded-lg border border-primary">
              <p className="text-sm text-academic-text-secondary">
                <strong className="text-primary">Performance:</strong> O Voting Classifier alcançou 88,2% de acurácia,
                com 100% dos erros ocorrendo entre classes adjacentes (comportamento seguro para sistema financeiro).
                Confiança média de 70% nas predições.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Dataset e Metodologia */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-academic-text mb-4">
              Dataset Híbrido e Metodologia
            </h2>
            <p className="text-xl text-academic-text-secondary max-w-3xl mx-auto">
              Combinação de dados reais internacionais com dados sintéticos brasileiros
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="card-academic p-6">
              <h3 className="text-xl font-bold mb-3 text-primary">Composição do Dataset</h3>
              <ul className="space-y-3 text-sm text-academic-text-secondary">
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">76%</span>
                  <span>Dados reais do <strong>Survey of Consumer Finances (SCF)</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">24%</span>
                  <span>Dados sintéticos adaptados ao contexto brasileiro</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">1.279</span>
                  <span>Registros totais após balanceamento via SMOTE</span>
                </li>
              </ul>
            </div>

            <div className="card-academic p-6">
              <h3 className="text-xl font-bold mb-3 text-primary">Validação Rigorosa</h3>
              <ul className="space-y-3 text-sm text-academic-text-secondary">
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Validação cruzada estratificada 5-fold</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Grid Search</strong> com 426 combinações</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Intervalo de confiança 95%</strong> via t-Student</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Seeds fixos</strong> para reprodutibilidade</span>
                </li>
              </ul>
            </div>

            <div className="card-academic p-6">
              <h3 className="text-xl font-bold mb-3 text-primary">Feature Engineering</h3>
              <ul className="space-y-3 text-sm text-academic-text-secondary">
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">15→26</span>
                  <span>Features expandidas via engenharia</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span>Features derivadas: <strong>patrimonio_sobre_renda</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Normalização Z-score</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-success">✓</span>
                  <span><strong>Label Encoding</strong> para categóricas</span>
                </li>
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Classes de Ativos */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card-academic p-8 mb-16"
        >
          <h2 className="text-3xl font-bold text-academic-text mb-6">6 Classes de Ativos</h2>
          <p className="text-academic-text-secondary mb-6">
            Portfólio diversificado cobrindo todas as principais categorias de investimento
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {assetClasses.map((asset, idx) => (
              <div key={idx} className="bg-academic-bg-secondary p-4 rounded-lg border border-academic-border">
                <h3 className="font-bold text-academic-text mb-1">{asset.title}</h3>
                <p className="text-sm text-academic-text-secondary">{asset.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Stack Tecnológica */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-academic-text mb-4">
              Stack Tecnológica
            </h2>
            <p className="text-xl text-academic-text-secondary max-w-3xl mx-auto">
              Tecnologias modernas e escaláveis para máximo desempenho
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="card-academic p-6">
              <h3 className="text-xl font-bold mb-4 text-primary">Backend</h3>
              <ul className="space-y-2">
                {techStack.backend.map((tech, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-academic-text-secondary">
                    <span className="text-success">✓</span>
                    <span>{tech}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="card-academic p-6">
              <h3 className="text-xl font-bold mb-4 text-primary">Frontend</h3>
              <ul className="space-y-2">
                {techStack.frontend.map((tech, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-academic-text-secondary">
                    <span className="text-success">✓</span>
                    <span>{tech}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="card-academic p-6">
              <h3 className="text-xl font-bold mb-4 text-primary">Machine Learning</h3>
              <ul className="space-y-2">
                {techStack.ml.map((tech, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-academic-text-secondary">
                    <span className="text-success">✓</span>
                    <span>{tech}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Conformidade Regulatória */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="card-academic p-8 mb-16"
        >
          <h2 className="text-3xl font-bold text-academic-text mb-6">
            Conformidade Regulatória
          </h2>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div className="bg-academic-bg-secondary p-6 rounded-lg border border-academic-border">
              <h3 className="text-xl font-bold text-primary mb-3">LGPD</h3>
              <p className="text-sm text-academic-text-secondary mb-3">
                Sistema em conformidade com a <strong>Lei Geral de Proteção de Dados (Lei 13.709/2018)</strong>:
              </p>
              <ul className="space-y-2 text-xs text-academic-text-secondary">
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

            <div className="bg-academic-bg-secondary p-6 rounded-lg border border-academic-border">
              <h3 className="text-xl font-bold text-primary mb-3">CVM 539/2013</h3>
              <p className="text-sm text-academic-text-secondary mb-3">
                Alinhamento com a <strong>Instrução CVM 539/2013</strong> sobre adequação de produtos:
              </p>
              <ul className="space-y-2 text-xs text-academic-text-secondary">
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

          <div className="bg-yellow-50 border-l-4 border-warning p-6 rounded-r-lg">
            <p className="text-sm text-academic-text-secondary">
              <strong className="text-warning">Aviso Educacional:</strong> Este é um sistema desenvolvido para fins
              acadêmicos (TCC - Sistemas de Informação). As recomendações são baseadas em modelos de IA e não constituem
              aconselhamento financeiro profissional. Sempre consulte um assessor certificado antes de investir.
            </p>
          </div>
        </motion.div>

        {/* CTA Final */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="card-academic p-12 text-center"
        >
          <h2 className="text-4xl font-bold text-academic-text mb-4">Experimente o Sistema</h2>
          <p className="text-xl text-academic-text-secondary mb-8 max-w-2xl mx-auto">
            Descubra seu perfil de investidor e receba uma carteira personalizada
            analisada por 7 modelos de Machine Learning
          </p>

          <button
            onClick={() => navigate('/questionario')}
            className="btn-primary text-xl px-12 py-5"
          >
            Começar Análise Gratuita
          </button>

          <p className="text-sm text-academic-text-muted mt-6">
            Gratuito • Sem cadastro • Resultados em 73ms
          </p>
        </motion.div>
      </div>

      {/* Footer */}
      <footer className="border-t border-academic-border bg-white mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-sm text-academic-text-secondary mb-2">
              <strong>Trabalho de Conclusão de Curso</strong> • Sistemas de Informação • IFES
            </p>
            <p className="text-xs text-academic-text-muted">
              Desenvolvido por Bruna Ribeiro Cedro • 2025
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
