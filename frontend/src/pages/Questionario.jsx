import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { classificarPerfil, recomendarPortfolio } from '../services/api';
import Loading from '../components/Loading';

export default function Questionario() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    // Passo 1: Dados Pessoais
    idade: '',
    renda_mensal: '',
    patrimonio_total: '',
    tem_reserva_emergencia: true,

    // Passo 2: Experiência e Conhecimento
    experiencia_investimento: '',
    conhecimento_mercado: 'basico',
    percentual_investir: '',

    // Passo 3: Objetivos
    objetivo_principal: 'crescimento_patrimonio',
    horizonte_investimento: '',
    tolerancia_risco: 'moderado',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Converter strings para números
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

      // PASSO 1: Primeiro classificar o perfil
      const perfilClassificado = await classificarPerfil(dados);

      // Salvar perfil e dados do formulário no localStorage
      localStorage.setItem('perfil_investidor', JSON.stringify(perfilClassificado));
      localStorage.setItem('dados_formulario', JSON.stringify(dados));

      // Ir para a página de perfil
      navigate('/perfil');

    } catch (err) {
      console.error('Erro ao processar:', err);
      setError('Erro ao processar suas informações. Verifique os dados e tente novamente.');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12">
        <Loading message="Classificando seu perfil de investidor..." />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Análise de Perfil</h1>
          <p className="text-gray-600">
            Responda as perguntas para receber uma recomendação personalizada
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Etapa {currentStep} de 3
            </span>
            <span className="text-sm text-gray-500">{Math.round((currentStep / 3) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / 3) * 100}%` }}
            />
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit}>
          {/* Passo 1: Dados Pessoais */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold mb-4">Dados Pessoais e Financeiros</h2>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Idade *
                </label>
                <input
                  type="number"
                  name="idade"
                  value={formData.idade}
                  onChange={handleChange}
                  required
                  min="18"
                  max="100"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Ex: 25"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Renda Mensal (R$) *
                </label>
                <input
                  type="number"
                  name="renda_mensal"
                  value={formData.renda_mensal}
                  onChange={handleChange}
                  required
                  min="0"
                  step="0.01"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Ex: 5000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Patrimônio Total (R$) *
                </label>
                <input
                  type="number"
                  name="patrimonio_total"
                  value={formData.patrimonio_total}
                  onChange={handleChange}
                  required
                  min="0"
                  step="0.01"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Ex: 50000"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Soma de todos os seus investimentos e poupança
                </p>
              </div>

              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="tem_reserva_emergencia"
                    checked={formData.tem_reserva_emergencia}
                    onChange={handleChange}
                    className="w-4 h-4 text-primary focus:ring-primary"
                  />
                  <span className="text-sm font-medium">
                    Tenho reserva de emergência (6 meses de despesas)
                  </span>
                </label>
              </div>
            </div>
          )}

          {/* Passo 2: Experiência */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold mb-4">Experiência e Conhecimento</h2>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Anos de Experiência com Investimentos *
                </label>
                <input
                  type="number"
                  name="experiencia_investimento"
                  value={formData.experiencia_investimento}
                  onChange={handleChange}
                  required
                  min="0"
                  max="50"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Ex: 2"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Pode ser 0 se for seu primeiro investimento
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Conhecimento do Mercado Financeiro *
                </label>
                <select
                  name="conhecimento_mercado"
                  value={formData.conhecimento_mercado}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                  <option value="nenhum">Nenhum conhecimento</option>
                  <option value="basico">Básico</option>
                  <option value="intermediario">Intermediário</option>
                  <option value="avancado">Avançado</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Percentual da Renda para Investir (%) *
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
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Ex: 20"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Quanto da sua renda mensal você pretende investir?
                </p>
              </div>
            </div>
          )}

          {/* Passo 3: Objetivos */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold mb-4">Objetivos de Investimento</h2>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Objetivo Principal *
                </label>
                <select
                  name="objetivo_principal"
                  value={formData.objetivo_principal}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                  <option value="preservacao_capital">Preservar Capital</option>
                  <option value="renda_passiva">Gerar Renda Passiva</option>
                  <option value="crescimento_patrimonio">Crescimento do Patrimônio</option>
                  <option value="aposentadoria">Aposentadoria</option>
                  <option value="compra_imovel">Compra de Imóvel</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Horizonte de Investimento (anos) *
                </label>
                <input
                  type="number"
                  name="horizonte_investimento"
                  value={formData.horizonte_investimento}
                  onChange={handleChange}
                  required
                  min="1"
                  max="50"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Ex: 10"
                />
                <p className="text-sm text-gray-500 mt-1">
                  Por quanto tempo pretende manter os investimentos?
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Tolerância ao Risco *
                </label>
                <select
                  name="tolerancia_risco"
                  value={formData.tolerancia_risco}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                  <option value="muito_conservador">Muito Conservador - Priorizo segurança total</option>
                  <option value="conservador">Conservador - Aceito pouco risco</option>
                  <option value="moderado">Moderado - Equilibro risco e retorno</option>
                  <option value="arrojado">Arrojado - Aceito mais risco por maior retorno</option>
                  <option value="muito_arrojado">Muito Arrojado - Busco máximo retorno</option>
                </select>
              </div>
            </div>
          )}

          {/* Buttons */}
          <div className="mt-8 flex justify-between">
            <button
              type="button"
              onClick={handlePrevious}
              disabled={currentStep === 1}
              className={`px-6 py-2 rounded-lg font-medium ${
                currentStep === 1
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              ← Anterior
            </button>

            {currentStep < 3 ? (
              <button
                type="button"
                onClick={handleNext}
                className="px-6 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700"
              >
                Próximo →
              </button>
            ) : (
              <button
                type="submit"
                className="px-8 py-2 bg-secondary text-white rounded-lg font-medium hover:bg-green-600"
              >
                🚀 Gerar Recomendação
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
