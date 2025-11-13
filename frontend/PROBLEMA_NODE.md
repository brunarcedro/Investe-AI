# ⚠️ PROBLEMA: Versão do Node.js

## Erro Encontrado

```
You are using Node.js 21.1.0.
Vite requires Node.js version 20.19+ or 22.12+.
```

## Soluções

### Opção 1: Atualizar Node.js (RECOMENDADO)

Baixar e instalar Node.js 22.x:
https://nodejs.org/

**Versão recomendada:** 22.12.0 LTS

### Opção 2: Usar versão antiga do Vite

```bash
cd frontend
npm uninstall vite @vitejs/plugin-react
npm install vite@^4.5.0 @vitejs/plugin-react@^4.2.0
npm run dev
```

### Opção 3: Usar NVM (Node Version Manager)

```bash
# Instalar NVM Windows
# https://github.com/coreybutler/nvm-windows

nvm install 22.12.0
nvm use 22.12.0
cd frontend
npm run dev
```

## Status Atual

- ✅ Backend API rodando em http://localhost:8000
- ✅ Frontend criado e configurado
- ❌ Frontend não inicia devido à versão do Node

## Próximos Passos

1. Escolher uma das opções acima
2. Rodar `npm run dev` no frontend
3. Acessar http://localhost:5173
