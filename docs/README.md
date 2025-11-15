# Documentação

Este diretório contém toda a documentação técnica do projeto.

## Índice

- **[Arquitetura](./architecture.md)** - Diagrama de arquitetura e visão geral do sistema
- **[Diagramas de Sequência](./sequence-diagrams.md)** - Fluxos principais da aplicação
- **[Guia de Desenvolvimento](./development.md)** - Setup, convenções e boas práticas
- **[Configuração do Banco de Dados](./database-setup.md)** - Setup completo do PostgreSQL e migrations
- **[Documentação da API](./api.md)** - Referência completa dos endpoints
- **[Quick Start](./quickstart.md)** - Guia rápido para começar

## Visão Geral

Este projeto implementa um backend para análise de sentimento, emoções e tópicos em publicações de redes sociais, utilizando:

- **FastAPI** para a API REST
- **SQLAlchemy 2.0** para acesso a dados
- **PostgreSQL** como banco de dados
- **Redis** para cache
- **Clean Architecture** como padrão arquitetural

## Começando

1. Leia o [Quick Start](./quickstart.md) para configurar o ambiente rapidamente
2. Consulte a [Configuração do Banco de Dados](./database-setup.md) para setup detalhado do PostgreSQL
3. Consulte a [Arquitetura](./architecture.md) para entender a estrutura
4. Veja os [Diagramas de Sequência](./sequence-diagrams.md) para entender os fluxos
5. Use a [Documentação da API](./api.md) como referência durante o desenvolvimento

## Contribuindo

Ao adicionar novas funcionalidades:

1. Atualize a documentação correspondente
2. Adicione diagramas se necessário
3. Mantenha os exemplos atualizados
4. Siga as convenções descritas no [Guia de Desenvolvimento](./development.md)

