import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { recomendarPortfolio } from '../services/api';
import Tooltip from '../components/Tooltip';

export default function Questionario() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);

  // Dados do formulário - TODAS AS 15 FEATURES DA REDE 1
  const [formData, setFormData] = useState({
    idade: 25,
    renda_mensal: 5000,
    dependentes: 0,
    estado_civil: 'solteiro',
    percentual_investir: 10,
    experiencia_investimento: 0,
    patrimonio_total: 0,
    dividas_percentual: 0,
    tolerancia_perda_1: 5,
    tolerancia_perda_2: 5,
    horizonte_investimento: 5,
    conhecimento_mercado: 'basico',
    estabilidade_emprego: 7,
    tem_reserva_emergencia: false,
    planos_grandes_gastos: 0,
    objetivo_principal: 'aumentar_patrimonio',
  });

  const sections = [
    {
      title: 'Dados Pessoais',
      description: 'Informações básicas sobre você',
      fields: [
        {
          name: 'idade',
          label: 'Qual a sua idade?',
          type: 'number',
          min: 18,
          max: 100,
          help: 'Sua idade influencia o horizonte de investimento recomendado'
        },
        {
          name: 'estado_civil',
          label: 'Estado Civil',
          type: 'select',
          options: [
            { value: 'solteiro', label: 'Solteiro(a)' },
            { value: 'casado', label: 'Casado(a)' },
            { value: 'divorciado', label: 'Divorciado(a)' },
            { value: 'viuvo', label: 'Viúvo(a)' }
          ]
        },
        {
          name: 'dependentes',
          label: 'Quantos dependentes você tem?',
          type: 'number',
          min: 0,
          max: 10,
          help: 'Filhos ou outras pessoas que dependem financeiramente de você'
        }
      ]
    },
    {
      title: 'Situação Financeira',
      description: 'Sua condição financeira atual',
      fields: [
        {
          name: 'renda_mensal',
          label: 'Renda Mensal (R$)',
          type: 'number',
          min: 0,
          step: 100,
          help: 'Soma de todas as suas fontes de renda mensais'
        },
        {
          name: 'patrimonio_total',
          label: 'Patrimônio Total (R$)',
          type: 'number',
          min: 0,
          step: 1000,
          help: 'Valor total dos seus bens e investimentos atuais'
        },
        {
          name: 'dividas_percentual',
          label: 'Percentual da renda comprometido com dívidas (%)',
          type: 'range',
          min: 0,
          max: 100,
          help: 'Quanto % da sua renda vai para pagar dívidas (financiamentos, empréstimos)'
        },
        {
          name: 'tem_reserva_emergencia',
          label: 'Possui reserva de emergência?',
          type: 'radio',
          options: [
            { value: true, label: 'Sim, tenho reserva equivalente a 6+ meses de despesas' },
            { value: false, label: 'Não, ainda não tenho reserva de emergência' }
          ],
          help: 'Recomenda-se ter 6 meses de despesas guardadas antes de investir'
        }
      ]
    },
    {
      title: 'Perfil de Investimento',
      description: 'Sua experiência e objetivos',
      fields: [
        {
          name: 'experiencia_investimento',
          label: 'Há quantos anos você investe?',
          type: 'number',
          min: 0,
          max: 50,
          help: 'Anos de experiência com investimentos (0 se nunca investiu)'
        },
        {
          name: 'conhecimento_mercado',
          label: 'Como você avalia seu conhecimento sobre investimentos?',
          type: 'select',
          options: [
            { value: 'nenhum', label: 'Nenhum - Estou começando agora' },
            { value: 'basico', label: 'Básico - Conheço o essencial' },
            { value: 'intermediario', label: 'Intermediário - Já invisto há um tempo' },
            { value: 'avancado', label: 'Avançado - Domino estratégias complexas' }
          ]
        },
        {
          name: 'horizonte_investimento',
          label: 'Por quanto tempo pretende manter o investimento (anos)?',
          type: 'number',
          min: 1,
          max: 50,
          help: 'Prazo até precisar resgatar o dinheiro'
        },
        {
          name: 'objetivo_principal',
          label: 'Qual seu principal objetivo?',
          type: 'select',
          options: [
            { value: 'aumentar_patrimonio', label: 'Aumentar meu patrimônio' },
            { value: 'aposentadoria', label: 'Construir aposentadoria' },
            { value: 'comprar_imovel', label: 'Comprar imóvel' },
            { value: 'educacao', label: 'Educação (própria ou filhos)' },
            { value: 'renda_passiva', label: 'Gerar renda passiva' }
          ]
        }
      ]
    },
    {
      title: 'Tolerância ao Risco',
      description: 'Como você reage a oscilações do mercado',
      fields: [
        {
          name: 'tolerancia_perda_1',
          label: 'Se seus investimentos caírem 10% em um mês, você:',
          type: 'range',
          min: 1,
          max: 10,
          labels: {
            1: 'Resgato tudo imediatamente',
            5: 'Aguardo e observo',
            10: 'Aproveito para investir mais'
          },
          help: 'Sua reação a uma queda de 10% no valor'
        },
        {
          name: 'tolerancia_perda_2',
          label: 'E se a queda for de 20%?',
          type: 'range',
          min: 1,
          max: 10,
          labels: {
            1: 'Resgato tudo com urgência',
            5: 'Fico preocupado mas aguardo',
            10: 'Vejo como oportunidade de compra'
          },
          help: 'Sua reação a uma queda de 20% no valor'
        }
      ]
    },
    {
      title: 'Planejamento',
      description: 'Sua situação e planos futuros',
      fields: [
        {
          name: 'percentual_investir',
          label: 'Qual % da sua renda pode investir mensalmente?',
          type: 'range',
          min: 0,
          max: 50,
          help: 'Percentual da renda disponível para aportes mensais'
        },
        {
          name: 'estabilidade_emprego',
          label: 'Como avalia a estabilidade do seu emprego/renda?',
          type: 'range',
          min: 1,
          max: 10,
          labels: {
            1: 'Muito instável',
            5: 'Razoavelmente estável',
            10: 'Muito estável'
          }
        },
        {
          name: 'planos_grandes_gastos',
          label: 'Planeja grandes gastos nos próximos 2 anos?',
          type: 'radio',
          options: [
            { value: 1, label: 'Sim (casamento, viagem, compra de carro, etc)' },
            { value: 0, label: 'Não' }
          ],
          help: 'Grandes despesas planejadas que podem exigir resgate dos investimentos'
        }
      ]
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    try {
      // Mapear estado civil para número
      const estadoCivilMap = {
        'solteiro': 0,
        'casado': 1,
        'divorciado': 2,
        'viuvo': 3
      };

      // API v3.0 PRECISA DE 15 FEATURES OBRIGATÓRIAS
      // Converter conhecimento_mercado para número (1-5)
      const conhecimentoMap = {
        'nenhum': 1,
        'basico': 2,
        'intermediario': 3,
        'avancado': 5
      };

      // Calcular valor_investir_mensal (percentual da renda)
      const valor_investir_mensal = (parseFloat(formData.renda_mensal) * parseFloat(formData.percentual_investir)) / 100;

      const apiData = {
        // 15 features obrigatórias (ordem exata do dataset de treinamento)
        idade: parseInt(formData.idade),
        renda_mensal: parseFloat(formData.renda_mensal),
        dependentes: parseInt(formData.dependentes),
        estado_civil: estadoCivilMap[formData.estado_civil] || 0,
        valor_investir_mensal: valor_investir_mensal,
        experiencia_anos: parseInt(formData.experiencia_investimento),
        dividas_percentual: parseFloat(formData.dividas_percentual),
        patrimonio_atual: parseFloat(formData.patrimonio_total),
        tolerancia_perda_1: parseInt(formData.tolerancia_perda_1),
        tolerancia_perda_2: parseInt(formData.tolerancia_perda_2),
        horizonte_investimento: parseInt(formData.horizonte_investimento),
        conhecimento_mercado: conhecimentoMap[formData.conhecimento_mercado] || 2,
        estabilidade_emprego: parseInt(formData.estabilidade_emprego),
        tem_reserva_emergencia: formData.tem_reserva_emergencia === 'true' || formData.tem_reserva_emergencia === true,
        planos_grandes_gastos: parseInt(formData.planos_grandes_gastos) > 0,

        // Opcionais para exibição na UI
        objetivo_principal: formData.objetivo_principal,
        percentual_investir: parseFloat(formData.percentual_investir)
      };

      console.log('Enviando dados completos:', apiData);

      const resultado = await recomendarPortfolio(apiData);

      localStorage.setItem('resultado_investimento', JSON.stringify(resultado));
      navigate('/resultado');

    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao processar. Verifique se o backend está rodando na porta 8000.');
    } finally {
      setLoading(false);
    }
  };

  const currentSection = sections[step];
  const isLastStep = step === sections.length - 1;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-academic-bg">
        <div className="text-center card-academic p-12 max-w-md">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="text-6xl mb-6"
          >
            🧠
          </motion.div>
          <h2 className="text-2xl font-bold text-academic-text mb-4">Processando análise...</h2>
          <p className="text-academic-text-secondary mb-2">Rede 1: Classificando perfil de risco</p>
          <p className="text-academic-text-secondary">Rede 2: Gerando alocação personalizada</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-academic-bg">
      {/* Header */}
      <header className="border-b border-academic-border bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link to="/" className="inline-flex items-center gap-2 text-primary hover:text-primary-dark transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span className="font-semibold">Voltar ao Início</span>
          </Link>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-academic-text">
              Etapa {step + 1} de {sections.length}
            </span>
            <span className="text-sm font-medium text-primary">
              {Math.round(((step + 1) / sections.length) * 100)}%
            </span>
          </div>
          <div className="w-full h-2 bg-academic-bg-secondary rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-primary"
              initial={{ width: 0 }}
              animate={{ width: `${((step + 1) / sections.length) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Form Card */}
        <motion.div
          key={step}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          className="card-academic p-8"
        >
          <h2 className="text-2xl font-bold text-academic-text mb-2">
            {currentSection.title}
          </h2>
          <p className="text-academic-text-secondary mb-8">
            {currentSection.description}
          </p>

          <form onSubmit={handleSubmit} className="space-y-6">
            {currentSection.fields.map((field) => (
              <div key={field.name}>
                <label className="block text-sm font-semibold text-academic-text mb-2">
                  <span className="flex items-center gap-2">
                    {field.label}
                    {field.help && (
                      <Tooltip content={field.help}>
                        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-primary-50 text-primary text-xs cursor-help">
                          ?
                        </span>
                      </Tooltip>
                    )}
                  </span>
                </label>

                {field.type === 'number' && (
                  <input
                    type="number"
                    value={formData[field.name]}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    min={field.min}
                    max={field.max}
                    step={field.step || 1}
                    className="input-clean w-full"
                    required
                  />
                )}

                {field.type === 'select' && (
                  <select
                    value={formData[field.name]}
                    onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                    className="input-clean w-full"
                    required
                  >
                    {field.options.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                )}

                {field.type === 'range' && (
                  <div>
                    <input
                      type="range"
                      value={formData[field.name]}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                      min={field.min}
                      max={field.max}
                      className="w-full h-2 bg-academic-bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                    />
                    <div className="flex justify-between mt-2 text-xs text-academic-text-muted">
                      {field.labels ? (
                        <>
                          <span>{field.labels[field.min]}</span>
                          <span className="font-bold text-primary text-base">{formData[field.name]}</span>
                          <span>{field.labels[field.max]}</span>
                        </>
                      ) : (
                        <>
                          <span>{field.min}</span>
                          <span className="font-bold text-primary text-base">{formData[field.name]}</span>
                          <span>{field.max}</span>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {field.type === 'radio' && (
                  <div className="space-y-3">
                    {field.options.map((opt) => (
                      <label
                        key={opt.value}
                        className="flex items-start gap-3 p-4 border-2 border-academic-border rounded-lg cursor-pointer hover:border-primary transition-colors"
                      >
                        <input
                          type="radio"
                          name={field.name}
                          value={opt.value}
                          checked={String(formData[field.name]) === String(opt.value)}
                          onChange={(e) => setFormData({ ...formData, [field.name]: opt.value })}
                          className="mt-1 text-primary focus:ring-primary"
                        />
                        <span className="text-sm text-academic-text">{opt.label}</span>
                      </label>
                    ))}
                  </div>
                )}

                {field.help && (
                  <p className="mt-2 text-xs text-academic-text-muted">
                    💡 {field.help}
                  </p>
                )}
              </div>
            ))}

            {/* Navigation Buttons */}
            <div className="flex gap-4 pt-6 border-t border-academic-border">
              {step > 0 && (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="btn-secondary flex-1"
                >
                  Voltar
                </button>
              )}

              {!isLastStep ? (
                <button
                  type="button"
                  onClick={() => setStep(step + 1)}
                  className="btn-primary flex-1"
                >
                  Próxima Etapa
                </button>
              ) : (
                <button
                  type="submit"
                  className="btn-primary flex-1"
                >
                  Gerar Recomendação com IA
                </button>
              )}
            </div>
          </form>
        </motion.div>

        {/* Info Footer */}
        <div className="mt-8 text-center text-sm text-academic-text-muted">
          <p>🔒 Seus dados são processados com segurança e não são armazenados permanentemente</p>
        </div>
      </div>
    </div>
  );
}
