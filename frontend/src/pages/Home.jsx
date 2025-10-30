import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { healthCheck } from '../services/api';

export default function Home() {
  const [apiStatus, setApiStatus] = useState(null);

  useEffect(() => {
    checkAPI();
  }, []);

  const checkAPI = async () => {
    try {
      const data = await healthCheck();
      setApiStatus(data);
    } catch (error) {
      console.error('API offline:', error);
      setApiStatus({ status: 'offline' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            💼 Investe-AI
          </h1>
          <p className="text-xl md:text-2xl mb-4">
            Sistema Inteligente de Recomendação de Carteiras de Investimento
          </p>
          <p className="text-lg mb-8 opacity-90">
            Usando Dupla Rede Neural para personalizar suas recomendações
          </p>

          <Link
            to="/questionario"
            className="inline-block bg-white text-primary px-8 py-4 rounded-lg text-lg font-bold hover:bg-gray-100 transition transform hover:scale-105"
          >
            🚀 Começar Análise
          </Link>

          {/* API Status */}
          {apiStatus && (
            <div className="mt-6">
              <span
                className={`inline-block px-4 py-2 rounded-full text-sm ${
                  apiStatus.status === 'online'
                    ? 'bg-green-500'
                    : 'bg-red-500'
                }`}
              >
                {apiStatus.status === 'online'
                  ? '✓ API Online'
                  : '✗ API Offline'}
              </span>
            </div>
          )}
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Por que usar o Investe-AI?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-5xl mb-4">🧠</div>
              <h3 className="text-xl font-bold mb-2">Dupla Rede Neural</h3>
              <p className="text-gray-600">
                Primeira rede classifica seu perfil de risco. Segunda rede
                recomenda alocação personalizada.
              </p>
            </div>

            <div className="text-center p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-5xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-2">91% de Acurácia</h3>
              <p className="text-gray-600">
                Supera trabalhos da literatura científica com classificação
                precisa e confiável.
              </p>
            </div>

            <div className="text-center p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-2">Recomendações Completas</h3>
              <p className="text-gray-600">
                Alocação detalhada, produtos específicos, métricas financeiras
                e alertas personalizados.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Como Funciona?
          </h2>

          <div className="max-w-3xl mx-auto space-y-6">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h4 className="font-bold text-lg mb-1">Responda o Questionário</h4>
                <p className="text-gray-600">
                  Informe seus dados pessoais, financeiros e objetivos de
                  investimento
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h4 className="font-bold text-lg mb-1">Análise por IA</h4>
                <p className="text-gray-600">
                  Duas redes neurais processam seus dados e geram recomendações
                  personalizadas
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h4 className="font-bold text-lg mb-1">Receba sua Carteira</h4>
                <p className="text-gray-600">
                  Veja seu perfil, alocação recomendada, produtos sugeridos e
                  métricas detalhadas
                </p>
              </div>
            </div>
          </div>

          <div className="text-center mt-12">
            <Link
              to="/questionario"
              className="inline-block bg-primary text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700 transition"
            >
              Começar Agora
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 bg-primary text-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">91%</div>
              <div className="text-blue-200">Acurácia</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">500+</div>
              <div className="text-blue-200">Análises Validadas</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">6</div>
              <div className="text-blue-200">Classes de Ativos</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">2</div>
              <div className="text-blue-200">Redes Neurais</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
