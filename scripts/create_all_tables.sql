-- Script SQL para criar todas as tabelas do banco de dados
-- Execute este script se as migrações não estiverem funcionando

-- Tabela publications (deve ser criada primeiro pois outras dependem dela)
CREATE TABLE IF NOT EXISTS publications (
    id SERIAL PRIMARY KEY,
    publicacao_n INTEGER NOT NULL UNIQUE,
    url VARCHAR NOT NULL,
    description TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    views VARCHAR,
    likes VARCHAR,
    comments_count INTEGER DEFAULT 0,
    shares VARCHAR,
    bookmarks VARCHAR,
    music_title VARCHAR,
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_publications_id ON publications(id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_publications_publicacao_n ON publications(publicacao_n);
CREATE INDEX IF NOT EXISTS ix_publications_date ON publications(date);

-- Tabela comments
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER NOT NULL,
    username VARCHAR NOT NULL,
    text TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comments_publication FOREIGN KEY (publication_id) REFERENCES publications(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_comments_id ON comments(id);
CREATE INDEX IF NOT EXISTS ix_comments_publication_id ON comments(publication_id);

-- Tabela replies
CREATE TABLE IF NOT EXISTS replies (
    id SERIAL PRIMARY KEY,
    comment_id INTEGER NOT NULL,
    username VARCHAR NOT NULL,
    text TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_replies_comment FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_replies_id ON replies(id);
CREATE INDEX IF NOT EXISTS ix_replies_comment_id ON replies(comment_id);

-- Tabela publication_analyses
CREATE TABLE IF NOT EXISTS publication_analyses (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER NOT NULL UNIQUE,
    main_sentiment VARCHAR NOT NULL,
    main_emotion VARCHAR NOT NULL,
    main_topic VARCHAR NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_publication_analyses_publication FOREIGN KEY (publication_id) REFERENCES publications(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_publication_analyses_id ON publication_analyses(id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_publication_analyses_publication_id ON publication_analyses(publication_id);

-- Tabela comment_analyses
CREATE TABLE IF NOT EXISTS comment_analyses (
    id SERIAL PRIMARY KEY,
    comment_id INTEGER NOT NULL UNIQUE,
    sentiment VARCHAR NOT NULL,
    emotion VARCHAR NOT NULL,
    topic VARCHAR NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comment_analyses_comment FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_comment_analyses_id ON comment_analyses(id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_comment_analyses_comment_id ON comment_analyses(comment_id);

-- Nota: A tabela users já foi criada anteriormente, então não precisa ser criada novamente aqui

