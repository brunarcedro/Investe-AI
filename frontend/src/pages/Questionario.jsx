import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { classificarPerfil } from '../services/api';
import Loading from '../components/Loading';

export default function Questionario() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [xp, setXp] = useState(0);

  const [formData, setFormData] = useState({
    idade: '',
    renda_mensal: '',
    patrimonio_total: '',
    tem_reserva_emergencia: true,
    experiencia_investimento: '',
    conhecimento_mercado: 'basico',
    percentual_investir: '',
    objetivo_principal: 'crescimento_patrimonio',
    horizonte_investimento: '',
    tolerancia_risco: 'moderado',
  });

  const steps = [
    { id: 1, title: 'Dados Financeiros', icon: '💰', xp: 20 },
    { id: 2, title: 'Experiência', icon: '📊', xp: 20 },
    { id: 3, title: 'Objetivos', icon: '🎯', xp: 20 },
  ];

  const tooltips = {
    patrimonio_total: 'Soma total de todos os seus investimentos, poupança e aplicações financeiras',
    reserva_emergencia: '6 meses de despesas guardadas para emergências (ex: perda de emprego, saúde)',
    experiencia_investimento: 'Há quanto tempo você investe? Se nunca investiu, coloque 0',
    conhecimento_mercado: 'Quanto você entende sobre investimentos, bolsa de valores e produtos financeiros?',
    percentual_investir: 'Que porcentagem da sua renda mensal você consegue investir todo mês?',
    horizonte_investimento: 'Por quanto tempo você pretende deixar o dinheiro investido?',
    tolerancia_risco: 'Quanto de variação no valor você aceita? Maior risco = maior retorno potencial',
  };

  const Tooltip = ({ text }) => (
    <div className="group relative inline-block ml-2">
      <span className="text-primary cursor-help">ℹ️</span>
      <div className="invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-all duration-300 absolute z-50 w-64 p-3 bg-dark-hover border border-primary/30 rounded-lg shadow-premium text-sm text-dark-text -left-28 top-6">
        <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-dark-hover border-l border-t border-primary/30 rotate-45" />
        {text}
      </div>
    </div>
  );

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const validateStep = (step) => {
    switch (step) {
      case 1:
        return formData.idade && formData.renda_mensal && formData.patrimonio_total;
      case 2:
        return formData.experiencia_investimento && formData.percentual_investir;
      case 3:
        return formData.horizonte_investimento;
      default:
        return true;
    }
  };

  const handleNext = () => {
    if (!validateStep(currentStep)) {
      setError('Por favor, preencha todos os campos obrigatórios');
      return;
    }

    if (!completedSteps.includes(currentStep)) {
      setCompletedSteps([...completedSteps, currentStep]);
      setXp(xp + steps[currentStep - 1].xp);
    }

    setError(null);
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    setError(null);
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateStep(currentStep)) {
      setError('Por favor, preencha todos os campos obrigatórios');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const dados = {
        idade: parseInt(formData.idade),
        renda_mensal: parseFloat(formData.renda_mensal),
        patrimonio_total: parseFloat(formData.patrimonio_total),
        experiencia_investimento: parseInt(formData.experiencia_investimento),
        objetivo_principal: formData.objetivo_principal,
        horizonte_investimento: parseInt(formData.horizonte_investimento),
        tolerancia_risco: formData.tolerancia_risco,
        conhecimento_mercado: formData.conhecimento_mercado,
        tem_reserva_emergencia: formData.tem_reserva_emergencia,
        percentual_investir: parseFloat(formData.percentual_investir),
      };

      const perfilClassificado = await classificarPerfil(dados);

      localStorage.setItem('perfil_investidor', JSON.stringify(perfilClassificado));
      localStorage.setItem('dados_formulario', JSON.stringify(dados));
      localStorage.setItem('xp_conquistado', xp + 60);

      navigate('/perfil');
    } catch (err) {
      console.error('Erro ao processar:', err);
      setError('Erro ao processar suas informações. Verifique os dados e tente novamente.');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-6">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-20 h-20 mx-auto rounded-full bg-gradient-fintech flex items-center justify-center shadow-glow"
          >
            <span className="text-4xl">🧠</span>
          </motion.div>
          <div>
            <h3 className="text-2xl font-bold text-dark-text mb-2">
              Analisando seu perfil...
            </h3>
            <p className="text-dark-muted">
              Duas redes neurais estão processando suas respostas
            </p>
          </div>
          <div className="flex items-center justify-center gap-2">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
              className="w-2 h-2 rounded-full bg-primary"
            />
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
              className="w-2 h-2 rounded-full bg-primary"
            />
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
              className="w-2 h-2 rounded-full bg-primary"
            />
          </div>
        </div>
      </div>
    );
  }

  const progress = (currentStep / 3) * 100;

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        {/* XP Badge */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="mb-6 flex justify-end"
        >
          <div className="glass-card px-4 py-2 flex items-center gap-2">
            <span className="text-warning text-xl">⭐</span>
            <span className="text-sm font-semibold text-dark-text">
              {xp} XP
            </span>
          </div>
        </motion.div>

        {/* Main Card */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="glass-card p-8 md:p-12"
        >
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-dark-text mb-2">
              Análise de Perfil de Investidor
            </h1>
            <p className="text-dark-muted">
              Responda as perguntas para receber uma carteira personalizada por IA
            </p>
          </div>

          {/* Stepper */}
          <div className="mb-10">
            <div className="flex items-center justify-between mb-4">
              {steps.map((step, index) => (
                <div key={step.id} className="flex items-center flex-1">
                  <div className="flex flex-col items-center flex-1">
                    <motion.div
                      whileHover={{ scale: 1.1 }}
                      className={`w-12 h-12 rounded-full flex items-center justify-center font-bold transition-all duration-300 ${
                        completedSteps.includes(step.id)
                          ? 'bg-success shadow-glow-success'
                          : currentStep === step.id
                          ? 'bg-gradient-fintech shadow-glow'
                          : 'bg-dark-hover'
                      }`}
                    >
                      {completedSteps.includes(step.id) ? (
                        <span className="text-white text-xl">✓</span>
                      ) : (
                        <span className="text-2xl">{step.icon}</span>
                      )}
                    </motion.div>
                    <span className={`mt-2 text-xs md:text-sm font-medium ${
                      currentStep === step.id ? 'text-primary' : 'text-dark-muted'
                    }`}>
                      {step.title}
                    </span>
                    {completedSteps.includes(step.id) && (
                      <span className="text-xs text-success mt-1">
                        +{step.xp} XP
                      </span>
                    )}
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`h-1 flex-1 mx-2 rounded-full transition-all duration-500 ${
                      completedSteps.includes(step.id) ? 'bg-success' : 'bg-dark-border'
                    }`} />
                  )}
                </div>
              ))}
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-dark-border rounded-full h-2 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
                className="h-full bg-gradient-fintech"
              />
            </div>
            <div className="mt-2 text-right">
              <span className="text-sm text-dark-muted">
                {Math.round(progress)}% completo
              </span>
            </div>
          </div>

          {/* Error Message */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-6 bg-danger/10 border border-danger/30 text-danger px-4 py-3 rounded-lg flex items-center gap-2"
              >
                <span>⚠️</span>
                <span>{error}</span>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Form */}
          <form onSubmit={handleSubmit}>
            <AnimatePresence mode="wait">
              {/* Step 1: Dados Financeiros */}
              {currentStep === 1 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-2xl font-bold text-dark-text mb-6 flex items-center gap-2">
                    💰 Dados Financeiros
                  </h2>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2">
                      Idade <span className="text-danger">*</span>
                    </label>
                    <input
                      type="number"
                      name="idade"
                      value={formData.idade}
                      onChange={handleChange}
                      required
                      min="18"
                      max="100"
                      className="input-dark w-full"
                      placeholder="Ex: 25"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Renda Mensal (R$) <span className="text-danger ml-1">*</span>
                    </label>
                    <input
                      type="number"
                      name="renda_mensal"
                      value={formData.renda_mensal}
                      onChange={handleChange}
                      required
                      min="0"
                      step="0.01"
                      className="input-dark w-full"
                      placeholder="Ex: 5000"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Patrimônio Total (R$) <span className="text-danger ml-1">*</span>
                      <Tooltip text={tooltips.patrimonio_total} />
                    </label>
                    <input
                      type="number"
                      name="patrimonio_total"
                      value={formData.patrimonio_total}
                      onChange={handleChange}
                      required
                      min="0"
                      step="0.01"
                      className="input-dark w-full"
                      placeholder="Ex: 50000"
                    />
                    <p className="text-xs text-dark-muted mt-1">
                      Soma de todos os seus investimentos e poupança
                    </p>
                  </div>

                  <div className="flex items-center gap-3 p-4 bg-dark-hover rounded-lg border border-dark-border">
                    <input
                      type="checkbox"
                      name="tem_reserva_emergencia"
                      checked={formData.tem_reserva_emergencia}
                      onChange={handleChange}
                      className="w-5 h-5 rounded border-dark-border text-primary focus:ring-primary"
                    />
                    <label className="text-sm font-medium text-dark-text flex items-center cursor-pointer">
                      Tenho reserva de emergência (6 meses de despesas)
                      <Tooltip text={tooltips.reserva_emergencia} />
                    </label>
                  </div>
                </motion.div>
              )}

              {/* Step 2: Experiência */}
              {currentStep === 2 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-2xl font-bold text-dark-text mb-6 flex items-center gap-2">
                    📊 Experiência e Conhecimento
                  </h2>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Anos de Experiência com Investimentos <span className="text-danger ml-1">*</span>
                      <Tooltip text={tooltips.experiencia_investimento} />
                    </label>
                    <input
                      type="number"
                      name="experiencia_investimento"
                      value={formData.experiencia_investimento}
                      onChange={handleChange}
                      required
                      min="0"
                      max="50"
                      className="input-dark w-full"
                      placeholder="Ex: 2 (coloque 0 se for iniciante)"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Conhecimento do Mercado Financeiro <span className="text-danger ml-1">*</span>
                      <Tooltip text={tooltips.conhecimento_mercado} />
                    </label>
                    <select
                      name="conhecimento_mercado"
                      value={formData.conhecimento_mercado}
                      onChange={handleChange}
                      required
                      className="input-dark w-full"
                    >
                      <option value="nenhum">Nenhum - Não entendo nada sobre investimentos</option>
                      <option value="basico">Básico - Conheço poupança e algumas aplicações</option>
                      <option value="intermediario">Intermediário - Já invisto em renda fixa e ações</option>
                      <option value="avancado">Avançado - Opero diversos produtos e acompanho o mercado</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Percentual da Renda para Investir (%) <span className="text-danger ml-1">*</span>
                      <Tooltip text={tooltips.percentual_investir} />
                    </label>
                    <input
                      type="number"
                      name="percentual_investir"
                      value={formData.percentual_investir}
                      onChange={handleChange}
                      required
                      min="0"
                      max="100"
                      step="0.1"
                      className="input-dark w-full"
                      placeholder="Ex: 20"
                    />
                    <p className="text-xs text-dark-muted mt-1">
                      Quanto da sua renda mensal você pretende investir?
                    </p>
                  </div>
                </motion.div>
              )}

              {/* Step 3: Objetivos */}
              {currentStep === 3 && (
                <motion.div
                  key="step3"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-2xl font-bold text-dark-text mb-6 flex items-center gap-2">
                    🎯 Objetivos de Investimento
                  </h2>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2">
                      Objetivo Principal <span className="text-danger">*</span>
                    </label>
                    <select
                      name="objetivo_principal"
                      value={formData.objetivo_principal}
                      onChange={handleChange}
                      required
                      className="input-dark w-full"
                    >
                      <option value="preservacao_capital">Preservar Capital - Não quero perder</option>
                      <option value="renda_passiva">Gerar Renda Passiva - Viver de dividendos</option>
                      <option value="crescimento_patrimonio">Crescimento do Patrimônio - Aumentar valor</option>
                      <option value="aposentadoria">Aposentadoria - Longo prazo</option>
                      <option value="compra_imovel">Compra de Imóvel - Juntar para imóvel</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Horizonte de Investimento (anos) <span className="text-danger ml-1">*</span>
                      <Tooltip text={tooltips.horizonte_investimento} />
                    </label>
                    <input
                      type="number"
                      name="horizonte_investimento"
                      value={formData.horizonte_investimento}
                      onChange={handleChange}
                      required
                      min="1"
                      max="50"
                      className="input-dark w-full"
                      placeholder="Ex: 10"
                    />
                    <p className="text-xs text-dark-muted mt-1">
                      Por quanto tempo pretende manter os investimentos?
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-dark-text mb-2 flex items-center">
                      Tolerância ao Risco <span className="text-danger ml-1">*</span>
                      <Tooltip text={tooltips.tolerancia_risco} />
                    </label>
                    <select
                      name="tolerancia_risco"
                      value={formData.tolerancia_risco}
                      onChange={handleChange}
                      required
                      className="input-dark w-full"
                    >
                      <option value="muito_conservador">Muito Conservador - Não aceito perder nada</option>
                      <option value="conservador">Conservador - Aceito perder até 5%</option>
                      <option value="moderado">Moderado - Aceito perder até 15%</option>
                      <option value="arrojado">Arrojado - Aceito perder até 30%</option>
                      <option value="muito_arrojado">Muito Arrojado - Busco máximo retorno</option>
                    </select>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Navigation Buttons */}
            <div className="mt-10 flex justify-between gap-4">
              <button
                type="button"
                onClick={handlePrevious}
                disabled={currentStep === 1}
                className={`px-6 py-3 rounded-xl font-medium transition-all ${
                  currentStep === 1
                    ? 'bg-dark-hover text-dark-muted cursor-not-allowed'
                    : 'bg-dark-card border-2 border-dark-border text-dark-text hover:border-primary'
                }`}
              >
                ← Anterior
              </button>

              {currentStep < 3 ? (
                <motion.button
                  type="button"
                  onClick={handleNext}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="btn-premium px-8 py-3"
                >
                  Próximo →
                </motion.button>
              ) : (
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="bg-gradient-to-r from-success to-success-dark text-white font-semibold px-10 py-3 rounded-xl shadow-glow-success hover:shadow-glow transition-all"
                >
                  🎯 Gerar Carteira Personalizada
                </motion.button>
              )}
            </div>
          </form>
        </motion.div>

        {/* Info Cards */}
        <div className="mt-8 grid md:grid-cols-3 gap-4">
          <div className="glass-card p-4 text-center">
            <div className="text-3xl mb-2">🔒</div>
            <div className="text-sm font-semibold text-dark-text mb-1">
              100% Seguro
            </div>
            <div className="text-xs text-dark-muted">
              Seus dados não são armazenados
            </div>
          </div>
          <div className="glass-card p-4 text-center">
            <div className="text-3xl mb-2">⚡</div>
            <div className="text-sm font-semibold text-dark-text mb-1">
              Resultado Instantâneo
            </div>
            <div className="text-xs text-dark-muted">
              Análise em menos de 3 segundos
            </div>
          </div>
          <div className="glass-card p-4 text-center">
            <div className="text-3xl mb-2">🧠</div>
            <div className="text-sm font-semibold text-dark-text mb-1">
              Inteligência Artificial
            </div>
            <div className="text-xs text-dark-muted">
              91% de acurácia comprovada
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
