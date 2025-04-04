# 🌱 HabitTracker

Plataforma web para **monitoramento de hábitos**, focada no bem-estar e na produtividade. Desenvolvida como projeto para a disciplina de Engenharia de Software.

## 📋 Objetivo

O HabitMaster tem como objetivo ajudar usuários a acompanhar hábitos diários e evoluir seus comportamentos por meio de metas, notificações e relatórios interativos.

---

## 🧩 Funcionalidades

- Cadastro e login de usuários
- Registro e acompanhamento de hábitos
- Lembretes personalizados
- Relatórios e gráficos de progresso
- Sistema de recompensas por metas concluídas (gamificação)
- Sugestões de melhoria baseadas em padrões de hábitos
- Detecção de correlações entre hábitos (ex: sono vs. produtividade)

---

## ⚙️ Tecnologias Utilizadas

### Front-end

- [Next.js](https://nextjs.org/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

### Back-end

- [FastAPI](https://fastapi.tiangolo.com/)
- [Python 3.10+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 🏗️ Estrutura do Projeto

```
backend/
├── app/
│   ├── api/               # Rotas da aplicação (controllers)
│   │   ├── routes/
│   │   │   └── habits.py  # Define os endpoints da API relacionados a hábitos
│   │   └── deps.py        # Dependências comuns para rotas (ex: autenticação)
│   │
│   ├── core/              # Configurações essenciais
│   │   ├── config.py      # Configurações do app (ex: variáveis de ambiente)
│   │   └── security.py    # Autenticação, tokens, senhas, etc
│   │
│   ├── models/            # Modelos do banco de dados (decidir qual escolher)
│   │   └── habit.py
│   │
│   ├── schemas/           # Validação e tipagem dos dados
│   │   └── habit.py       # Algo como HabitCreate, HabitResponse, etc.
│   │
│   ├── services/          # Lógica de negócio
│   │   └── habit_service.py  # Regras como "se hábito X for feito Y vezes, dar recompensa"
│   │
│   ├── db/                # Conexão com banco e utilitários
│   │   ├── base.py
│   │   └── session.py
│   │
│   └── main.py            # Inicialização da aplicação FastAPI
│
frontend/
├── public/                 # Arquivos públicos (imagens, ícones etc.)
├── src/
│   ├── pages/              # Rotas do app (ex: index.tsx, dashboard.tsx)
│   ├── components/         # Componentes reutilizáveis (botões, cards etc.)
│   ├── services/           # Requisições HTTP ao back-end
│   │   └── api.ts          # Configuração base do axios/fetch
│   ├── contexts/           # Contextos globais (ex: auth)
│   ├── styles/             # Arquivos CSS ou Tailwind configs
│   └── utils/              # Funções auxiliares (ex: formatação de datas)
├── tailwind.config.js      # Configurações do Tailwind (se usar)
├── .env.local              # Variáveis de ambiente
└── next.config.js          # Configurações do Next.js
```

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Node.js >=18
- Python >=3.10
- PostgreSQL

### 🔧 Instalação

#### Back-end

**A DEFINIR**

#### Front-end

```bash
cd frontend
pnpm install
pnpm run dev
```
##### *OBS ->* verificar a instalação do pnpm(gerenciador de pacotes)

Acesse em: [http://localhost:3000](http://localhost:3000)

---

## 🔗 Integração Front-end & Back-end

As requisições do front são feitas via \`fetch\` ou \`axios\` para o back-end (FastAPI/Flask), por exemplo:

\`\`\`js
const response = await axios.post('http://localhost:8000/api/habits', {
  name: 'Estudar 30 minutos',
  category: 'Produtividade',
})
\`\`\`

---

## ✍️ Convenção de Commits

Sugestão do padrão **Conventional Commits**:

### 💡 Formato

\`\`\`
<tipo>(escopo): descrição
\`\`\`

### 📦 Tipos

| Tipo       | Descrição                             |
|------------|----------------------------------------|
| \`feat\`     | Nova funcionalidade                    |
| \`fix\`      | Correção de bug                        |
| \`docs\`     | Atualização de documentação            |
| \`style\`    | Mudanças visuais ou de formatação      |
| \`refactor\` | Refatoração de código (sem novo recurso) |
| \`test\`     | Adição/modificação de testes           |
| \`chore\`    | Tarefas de manutenção/configuração     |

### ✅ Exemplos

```
feat(frontend): adicionar tela de criação de hábito
fix(backend): corrigir erro ao criar hábito com nome vazio
docs: atualizar instruções de instalação no README
```

---

## 🪄 Organização de Branches

- \`main\`: versão estável
- \`dev\`: branch de integração
- \`frontend/feature-nome\`: desenvolvimento de funcionalidades no front-end
- \`backend/feature-nome\`: desenvolvimento de funcionalidades no back-end

---

## 📅 Status

Projeto em desenvolvimento 🚧
