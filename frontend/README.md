# 🌐 Frontend Investe-AI

Sistema web de recomendação de carteiras de investimento com dupla rede neural.

## 🚀 Stack Tecnológica

- **React 18** - Biblioteca UI
- **Vite 4.5** - Build tool ultra-rápida
- **Tailwind CSS** - Estilização utility-first
- **React Router** - Navegação SPA
- **Axios** - Cliente HTTP
- **Recharts** - Gráficos (a ser implementado)
- **React Hook Form** - Formulários (a ser implementado)

## ⚙️ Como Rodar

```bash
# 1. Instalar dependências
npm install

# 2. Rodar em desenvolvimento
npm run dev

# 3. Abrir navegador
# http://localhost:5173
```

## 🔌 Integração com Backend

O frontend se conecta com a API em `http://localhost:8000`

**Importante:** Backend deve estar rodando!

```bash
# Em outro terminal
cd ../backend
python api/main.py
```

## 📱 Páginas

- ✅ **Home** - Landing page (http://localhost:5173)
- ✅ **Sobre** - Informações do projeto (http://localhost:5173/sobre)
- ⏳ **Questionário** - A implementar
- ⏳ **Resultado** - A implementar

## 🎨 Tema

Cores definidas em `tailwind.config.js`:
- Primary: #0066FF (azul)
- Secondary: #00C853 (verde)
- Dark: #1A1A2E
- Light: #F5F7FA

## 📦 Scripts

```bash
npm run dev      # Desenvolvimento
npm run build    # Build para produção
npm run preview  # Preview do build
```

---

**Desenvolvido por:** Bruna Ribeiro Cedro
**TCC - Sistemas de Informação - IFES**
