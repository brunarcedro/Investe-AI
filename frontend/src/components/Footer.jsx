export default function Footer() {
  return (
    <footer className="bg-dark text-white mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">💼 Investe-AI</h3>
            <p className="text-gray-300">
              Sistema Inteligente de Recomendação de Carteiras de Investimento
            </p>
          </div>

          <div>
            <h4 className="font-bold mb-4">Tecnologia</h4>
            <ul className="text-gray-300 space-y-2">
              <li>✓ Dupla Rede Neural</li>
              <li>✓ 91% de Acurácia</li>
              <li>✓ Recomendações Personalizadas</li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold mb-4">TCC</h4>
            <p className="text-gray-300">
              Sistemas de Informação - IFES<br />
              Desenvolvido por Bruna Ribeiro Cedro<br />
              2025
            </p>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
          <p>&copy; 2025 Investe-AI. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
}
