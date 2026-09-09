# 📚 Engineering Study App

Um aplicativo multiplataforma para estudantes de engenharia, com explicações detalhadas de disciplinas, fórmulas, exercícios e resoluções.

## 🎯 Objetivo

Criar uma plataforma educativa completa que ajude estudantes de engenharia a compreender melhor os conceitos, fórmulas e suas aplicações práticas através de exercícios resolvidos.

## ✨ Funcionalidades

- 📖 **Disciplinas Explicadas**: Todas as principais matérias de engenharia com conteúdo detalhado
- 🧮 **Fórmulas Documentadas**: Cada fórmula com explicação de componentes e como utilizá-la
- 📝 **Exercícios**: Problemas práticos com diferentes níveis de dificuldade
- ✅ **Resoluções Passo a Passo**: Soluções detalhadas para cada exercício
- 📱 **Multiplataforma**: Acesso via web, mobile (iOS/Android) e desktop

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: FastAPI (Python)
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **API**: RESTful com documentação automática

### Frontend (Em desenvolvimento)
- **Web**: React / Vue.js
- **Mobile**: React Native ou Flutter
- **Desktop**: Electron

## 📁 Estrutura do Projeto

```
engineering-study-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── database.py
│   ├── tests/
│   ├── migrations/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── web/
│   ├── mobile/
│   └── desktop/
├── docs/
├── .gitignore
└── README.md
```

## 🚀 Como Começar

### Pré-requisitos
- Python 3.10+
- PostgreSQL
- Git

### Instalação do Backend

1. Clone o repositório:
```bash
git clone https://github.com/Nycholasbarros/engineering-study-app.git
cd engineering-study-app/backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env`:
```bash
cp .env.example .env
```

5. Configure as variáveis de ambiente no arquivo `.env`

6. Execute as migrações do banco de dados:
```bash
alembic upgrade head
```

7. Inicie o servidor:
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 📚 Disciplinas Planejadas

- [ ] Cálculo (Cálculo I, II, III, IV)
- [ ] Álgebra Linear
- [ ] Física (Mecânica, Eletromagnetismo, Ondas)
- [ ] Química
- [ ] Mecânica dos Fluidos
- [ ] Resistência dos Materiais
- [ ] Termodinâmica
- [ ] Eletricidade e Magnetismo
- [ ] Equações Diferenciais
- [ ] Programação

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**Nycharlas Barros** - [GitHub](https://github.com/Nycholasbarros)

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/Nycholasbarros/engineering-study-app/issues) no repositório.

---

**Status**: 🔄 Em Desenvolvimento

Última atualização: 2026-09-09
