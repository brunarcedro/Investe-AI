export default function Sobre() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Sobre o Projeto</h1>

      <div className="prose max-w-none">
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">🎓 Trabalho de Conclusão de Curso</h2>
          <p className="text-gray-700 mb-4">
            Este sistema foi desenvolvido como Trabalho de Conclusão de Curso (TCC)
            do curso de Sistemas de Informação do IFES (Instituto Federal do Espírito Santo).
          </p>
          <div className="bg-gray-50 p-6 rounded-lg">
            <p><strong>Desenvolvido por:</strong> Bruna Ribeiro Cedro</p>
            <p><strong>Instituição:</strong> IFES - Instituto Federal do Espírito Santo</p>
            <p><strong>Curso:</strong> Sistemas de Informação</p>
            <p><strong>Ano:</strong> 2025</p>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">🧠 Tecnologia</h2>
          <p className="text-gray-700 mb-4">
            O Investe-AI utiliza uma arquitetura de <strong>dupla rede neural</strong>:
          </p>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div className="border border-blue-200 bg-blue-50 p-6 rounded-lg">
              <h3 className="font-bold text-lg mb-2">1ª Rede Neural</h3>
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                <li>Classifica perfil de risco</li>
                <li>15 features de entrada</li>
                <li>91% de acurácia</li>
                <li>Cohen's Kappa: 0.80</li>
              </ul>
            </div>

            <div className="border border-green-200 bg-green-50 p-6 rounded-lg">
              <h3 className="font-bold text-lg mb-2">2ª Rede Neural</h3>
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                <li>Recomenda alocação</li>
                <li>8 features de entrada</li>
                <li>R² &gt; 0.85</li>
                <li>6 classes de ativos</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">📊 Classes de Ativos</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="border p-4 rounded-lg">
              <h4 className="font-bold mb-2">💰 Renda Fixa</h4>
              <p className="text-sm text-gray-600">
                Tesouro Direto, CDB, LCI/LCA
              </p>
            </div>
            <div className="border p-4 rounded-lg">
              <h4 className="font-bold mb-2">📈 Ações Brasil</h4>
              <p className="text-sm text-gray-600">
                Bovespa, ETFs, Ações individuais
              </p>
            </div>
            <div className="border p-4 rounded-lg">
              <h4 className="font-bold mb-2">🌎 Ações Internacional</h4>
              <p className="text-sm text-gray-600">
                S&P 500, ETFs globais, BDRs
              </p>
            </div>
            <div className="border p-4 rounded-lg">
              <h4 className="font-bold mb-2">🏢 Fundos Imobiliários</h4>
              <p className="text-sm text-gray-600">
                FIIs de tijolo, papel, logística
              </p>
            </div>
            <div className="border p-4 rounded-lg">
              <h4 className="font-bold mb-2">⚡ Commodities</h4>
              <p className="text-sm text-gray-600">
                Ouro, petróleo, mineradoras
              </p>
            </div>
            <div className="border p-4 rounded-lg">
              <h4 className="font-bold mb-2">₿ Criptomoedas</h4>
              <p className="text-sm text-gray-600">
                Bitcoin, Ethereum, ETFs cripto
              </p>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-4">🎯 Validação</h2>
          <p className="text-gray-700 mb-4">
            O sistema foi validado por especialista certificado CFP®/CGA seguindo
            as normas da CVM 539/2013 para suitability de investimentos.
          </p>
          <div className="bg-green-50 border border-green-200 p-6 rounded-lg">
            <p className="font-bold mb-2">Métricas de Validação:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>500 casos validados por especialista</li>
              <li>Acurácia de 91% na classificação</li>
              <li>Precision: 89%</li>
              <li>Recall: 88%</li>
            </ul>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold mb-4">💻 Stack Tecnológica</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-bold mb-2">Backend</h3>
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                <li>Python 3.11</li>
                <li>FastAPI</li>
                <li>scikit-learn (MLPClassifier, MLPRegressor)</li>
                <li>pandas, numpy</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold mb-2">Frontend</h3>
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                <li>React 18</li>
                <li>Vite</li>
                <li>Tailwind CSS</li>
                <li>Recharts</li>
                <li>Axios</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
