# Instruções para Compilar a Seção de Resultados

## Pacotes Necessários no Preâmbulo

Adicione os seguintes pacotes no preâmbulo do seu documento principal (antes de `\begin{document}`):

```latex
\usepackage{amssymb}      % Para o símbolo \checkmark
\usepackage{booktabs}     % Para toprule, midrule, bottomrule
\usepackage{graphicx}     % Para incluir figuras
```

Se você já tem esses pacotes, não precisa adicionar novamente.

## Problemas Corrigidos

### 1. Símbolo \checkmark
**Erro original:**
```
Undefined control sequence \checkmark
```

**Solução:**
- Adicionado `\usepackage{amssymb}` no preâmbulo
- Todos os `\checkmark` foram colocados em modo matemático: `$\checkmark$`

### 2. Figuras Comentadas
As referências a figuras foram temporariamente comentadas porque os arquivos de imagem não existem no Overleaf.

**Para habilitar as figuras:**
1. Faça upload das imagens para a pasta `figuras/` no Overleaf
2. Descomente os blocos `\begin{figure}...\end{figure}`

### 3. Caracteres Unicode
Se houver erros com caracteres especiais como ≤, substitua por comandos LaTeX:
- `≤` → `\leq`
- `≥` → `\geq`
- `±` → `\pm`

## Como Incluir o Arquivo no seu TCC

No seu arquivo principal (provavelmente `ifes.tex` ou similar), adicione onde quiser a seção de resultados:

```latex
\input{secao_resultados}
```

## Compile Timeout

Se você está tendo **timeout de compilação no Overleaf (plano gratuito)**, tente:

1. **Comentar todas as figuras temporariamente** (já feito)
2. **Reduzir o tamanho/resolução das imagens**
3. **Habilitar "Fast [draft] mode"**:
   - Clique em "Recompile"
   - Selecione "Fast [draft] mode"
4. **Dividir o documento em partes menores**
5. **Considerar upgrade do plano** se o documento for muito grande

## Estrutura das Tabelas

Todas as tabelas usam o pacote `booktabs` com:
- `\toprule` - linha superior
- `\midrule` - linha do meio
- `\bottomrule` - linha inferior

Exemplo:
```latex
\begin{table}[htbp]
\centering
\caption{Título da tabela}
\label{tab:nome_label}
\begin{tabular}{lcc}
\toprule
\textbf{Coluna 1} & \textbf{Coluna 2} & \textbf{Coluna 3} \\ \midrule
Dado 1 & Dado 2 & Dado 3 \\
\bottomrule
\end{tabular}
\end{table}
```

## Verificar Compilação

Após adicionar o `\usepackage{amssymb}`, seu documento deve compilar sem erros relacionados à seção de resultados.

Se ainda houver problemas, verifique:
1. ✅ Pacote `amssymb` está no preâmbulo
2. ✅ Pacote `booktabs` está no preâmbulo
3. ✅ Figuras estão comentadas ou os arquivos existem
4. ✅ Não há outros erros no documento principal
