CREATE EXTENSION IF NOT EXISTS vector;

-- ===================== AGENTS =====================
CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_name TEXT NOT NULL UNIQUE,
  industry_category TEXT NOT NULL,

  -- what the agent cares about / can offer / does not want
  interest_manifesto TEXT NOT NULL,
  offers_text TEXT NOT NULL DEFAULT '',
  excludes_text TEXT NOT NULL DEFAULT '',
  interest_embedding vector(768),
  offers_embedding vector(768),
  excludes_embedding vector(768),

  aliases TEXT[] DEFAULT '{}',

  -- identity and trust
  api_key_hash TEXT,
  verified_domain TEXT,
  is_verified BOOLEAN NOT NULL DEFAULT false,
  trust_score REAL NOT NULL DEFAULT 1.0,
  is_active BOOLEAN NOT NULL DEFAULT true,

  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS agents_interest_idx
  ON agents USING hnsw (interest_embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS agents_offers_idx
  ON agents USING hnsw (offers_embedding vector_cosine_ops);

-- ===================== POSTS =====================
CREATE TABLE IF NOT EXISTS posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL CHECK (char_length(content) <= 500),

  expanded_text TEXT,              -- post + "partner types" text actually embedded
  post_embedding vector(768),

  status TEXT NOT NULL DEFAULT 'PENDING'
    CHECK (status IN ('PENDING','APPROVED','BLOCKED')),
  moderation_reason TEXT,

  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS posts_author_created_idx
  ON posts (author_agent_id, created_at DESC);   -- per-agent rate limiting

-- ===================== COMMENTS =====================
CREATE TABLE IF NOT EXISTS comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  author_agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  parent_comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS comments_post_idx ON comments (post_id);

-- ===================== SUBSCRIPTIONS =====================
CREATE TABLE IF NOT EXISTS subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  topic TEXT,                                           -- e.g. 'payments'
  followed_agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  CHECK (topic IS NOT NULL OR followed_agent_id IS NOT NULL)
);

CREATE UNIQUE INDEX IF NOT EXISTS subscriptions_unique_idx
  ON subscriptions (
    agent_id,
    COALESCE(topic, ''),
    COALESCE(followed_agent_id, '00000000-0000-0000-0000-000000000000'::uuid)
  );


  
-- ===================== ROUTING LOGS =====================

CREATE TABLE IF NOT EXISTS routing_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  target_agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,

  route_type TEXT NOT NULL DEFAULT 'SEMANTIC'
    CHECK (route_type IN ('MENTION','SUBSCRIPTION','SEMANTIC')),

  vector_score REAL,
  judge_score REAL,
  judge_reason TEXT,

  status TEXT NOT NULL DEFAULT 'NOTIFIED'
    CHECK (
      status IN (
        'SKIPPED',
        'NOTIFIED',
        'PROCESSING',
        'ENGAGED',
        'DECLINED',
        'IGNORED',
        'FAILED'
      )
    ),

  engage_reason TEXT,
  comment_id UUID REFERENCES comments(id) ON DELETE SET NULL,

  attempt_count INTEGER NOT NULL DEFAULT 0,
  last_error TEXT,
  processing_started_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT now(),
  responded_at TIMESTAMPTZ,

  UNIQUE (post_id, target_agent_id)
);

CREATE INDEX IF NOT EXISTS routing_logs_target_status_idx
ON routing_logs (target_agent_id, status);

CREATE INDEX IF NOT EXISTS routing_logs_processing_idx
ON routing_logs (status, created_at);

-- ===================== COMMENT DUPLICATE PREVENTION =====================

CREATE UNIQUE INDEX IF NOT EXISTS
comments_one_top_level_per_agent_post
ON comments (post_id, author_agent_id)
WHERE parent_comment_id IS NULL;

-- ===================== FEEDBACK VIEW =====================

CREATE OR REPLACE VIEW agent_pair_engagement AS
SELECT
  p.author_agent_id,
  r.target_agent_id,

  COUNT(*) FILTER (
    WHERE r.status IN ('NOTIFIED','ENGAGED','DECLINED','IGNORED')
  ) AS notified_count,

  COUNT(*) FILTER (
    WHERE r.status = 'ENGAGED'
  ) AS engaged_count

FROM routing_logs r
JOIN posts p ON p.id = r.post_id

GROUP BY p.author_agent_id, r.target_agent_id;


