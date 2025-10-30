import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { recomendarPortfolio } from '../services/api';
import Loading from '../components/Loading';

export default function Perfil() {
  const navigate = useNavigate();
  const [perfilData, setPerfilData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Carregar dados do perfil do localStorage
    const data = localStorage.getItem('perfil_investidor');
    if (data) {
      setPerfilData(JSON.parse(data));
    } else {
      // Se não houver dados, redirecionar para questionário
      navigate('/questionario');
    }
  }, [navigate]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12">
        <Loading message="Gerando sua carteira personalizada..." />
      </div>
    );
  }

  if (!perfilData) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="text-center">
          <p>Carregando seu perfil...</p>
        </div>
      </div>
    );
  }

  // Determinar cor e ícone baseado no perfil
  const getPerfilStyle = (perfil) => {
    if (perfil.includes('Conservador')) {
      return {
        color: 'text-blue-600',
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        icon: '🛡️',
        gradient: 'from-blue-400 to-blue-600'
      };
    } else if (perfil.includes('Moderado')) {
      return {
        color: 'text-yellow-600',
        bg: 'bg-yellow-50',
        border: 'border-yellow-200',
        icon: '⚖️',
        gradient: 'from-yellow-400 to-orange-600'
      };
    } else if (perfil.includes('Arrojado')) {
      return {
        color: 'text-red-600',
        bg: 'bg-red-50',
        border: 'border-red-200',
        icon: '🚀',
        gradient: 'from-red-400 to-red-600'
      };
    }
    return {
      color: 'text-gray-600',
      bg: 'bg-gray-50',
      border: 'border-gray-200',
      icon: '📊',
      gradient: 'from-gray-400 to-gray-600'
    };
  };

  const style = getPerfilStyle(perfilData.perfil);

  // Descrições detalhadas por perfil
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
      retornoEsperado: '100% - 110% do CDI ao ano',
      riscoEsperado: 'Muito Baixo',
      perfisAdequados: ['Aposentados', 'Iniciantes', 'Reserva de emergência']
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
      retornoEsperado: '110% - 130% do CDI ao ano',
      riscoEsperado: 'Baixo',
      perfisAdequados: ['Investidores cautelosos', 'Aposentadoria próxima', 'Objetivos de curto prazo']
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
      perfisAdequados: ['Investidores equilibrados', 'Construção de patrimônio', 'Jovens e adultos']
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
      perfisAdequados: ['Investidores experientes', 'Jovens com horizonte longo', 'Alta tolerância emocional']
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
      perfisAdequados: ['Especialistas', 'Jovens com reserva consolidada', 'Alta capacidade de recuperação']
    }
  };

  const detalhes = descricoesPerfil[perfilData.perfil] || descricoesPerfil['Moderado'];

  const handleContinuar = async () => {
    setLoading(true);

    try {
      // Recuperar dados do formulário
      const dadosFormulario = localStorage.getItem('dados_formulario');
      if (!dadosFormulario) {
        navigate('/questionario');
        return;
      }

      const dados = JSON.parse(dadosFormulario);

      // PASSO 2: Agora gerar a recomendação de carteira
      const resultado = await recomendarPortfolio(dados);

      // Salvar resultado no localStorage
      localStorage.setItem('resultado_investimento', JSON.stringify(resultado));

      // Ir para a página de resultado
      navigate('/resultado');
    } catch (error) {
      console.error('Erro ao gerar recomendação:', error);
      setLoading(false);
      alert('Erro ao gerar recomendação. Tente novamente.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header com animação */}
        <div className={`bg-gradient-to-r ${style.gradient} text-white rounded-2xl p-8 mb-8 shadow-xl`}>
          <div className="text-center">
            <div className="text-6xl mb-4 animate-bounce">{style.icon}</div>
            <h1 className="text-4xl font-bold mb-2">Seu Perfil de Investidor</h1>
            <div className="text-5xl font-extrabold my-6">
              {perfilData.perfil}
            </div>
            <p className="text-xl opacity-90">
              Score de Risco: {(perfilData.score_risco * 100).toFixed(0)}%
            </p>
          </div>
        </div>

        {/* Resumo do Perfil */}
        <div className={`${style.bg} border-2 ${style.border} rounded-xl p-6 mb-6`}>
          <h2 className="text-2xl font-bold mb-3 flex items-center">
            <span className="text-3xl mr-3">💡</span>
            O que isso significa?
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed">
            {detalhes.resumo}
          </p>
        </div>

        {/* Características do seu perfil */}
        <div className="bg-white border-2 border-gray-200 rounded-xl p-6 mb-6 shadow-md">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <span className="text-3xl mr-3">✨</span>
            Características do seu perfil
          </h2>
          <ul className="space-y-3">
            {detalhes.caracteristicas.map((caract, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-green-500 text-xl mr-3 mt-1">✓</span>
                <span className="text-gray-700">{caract}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Suas características pessoais */}
        {perfilData.caracteristicas && perfilData.caracteristicas.length > 0 && (
          <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6 mb-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center text-blue-800">
              <span className="text-3xl mr-3">👤</span>
              Sobre você
            </h2>
            <ul className="space-y-2">
              {perfilData.caracteristicas.map((caract, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-blue-500 text-xl mr-3">•</span>
                  <span className="text-gray-700">{caract}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Investimentos típicos */}
        <div className="bg-white border-2 border-gray-200 rounded-xl p-6 mb-6 shadow-md">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <span className="text-3xl mr-3">📊</span>
            Investimentos típicos para seu perfil
          </h2>
          <div className="grid md:grid-cols-2 gap-3">
            {detalhes.investimentos.map((inv, idx) => (
              <div key={idx} className="flex items-center bg-gray-50 rounded-lg p-3">
                <span className="text-primary text-xl mr-3">→</span>
                <span className="font-medium text-gray-700">{inv}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Expectativas */}
        <div className="grid md:grid-cols-3 gap-4 mb-8">
          <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4">
            <div className="text-green-600 text-sm font-bold mb-2">RETORNO ESPERADO</div>
            <div className="text-2xl font-bold text-green-700">{detalhes.retornoEsperado}</div>
          </div>

          <div className="bg-orange-50 border-2 border-orange-200 rounded-xl p-4">
            <div className="text-orange-600 text-sm font-bold mb-2">NÍVEL DE RISCO</div>
            <div className="text-2xl font-bold text-orange-700">{detalhes.riscoEsperado}</div>
          </div>

          <div className="bg-purple-50 border-2 border-purple-200 rounded-xl p-4">
            <div className="text-purple-600 text-sm font-bold mb-2">ADEQUADO PARA</div>
            <div className="text-sm font-medium text-purple-700">
              {detalhes.perfisAdequados.join(', ')}
            </div>
          </div>
        </div>

        {/* Descrição adicional */}
        {perfilData.descricao && (
          <div className="bg-gray-50 border-l-4 border-primary rounded-lg p-6 mb-8">
            <p className="text-gray-700 italic">
              "{perfilData.descricao}"
            </p>
          </div>
        )}

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-primary to-blue-600 rounded-xl p-8 text-center text-white mb-6">
          <h2 className="text-2xl font-bold mb-3">Pronto para ver sua carteira personalizada?</h2>
          <p className="text-lg mb-6 opacity-90">
            Agora que você conhece seu perfil, vamos montar uma carteira ideal para você!
          </p>
          <button
            onClick={handleContinuar}
            className="bg-white text-primary px-8 py-4 rounded-lg text-lg font-bold hover:bg-gray-100 transition transform hover:scale-105 shadow-lg"
          >
            🎯 Ver Minha Carteira Recomendada
          </button>
        </div>

        {/* Aviso */}
        <div className="text-center text-sm text-gray-500">
          <p>
            💡 A carteira será montada especificamente para o perfil <strong>{perfilData.perfil}</strong>
          </p>
        </div>
      </div>
    </div>
  );
}
