-- Painel de Reação do Culto: só números agregados. Nenhum campo por pessoa (tests/test_schema.py verifica).
-- Projeto Supabase criado na região South America (São Paulo).
create table if not exists service (
  culto text primary key, data date, horario text, pregador text, fonte text, observacoes text, created_at timestamptz default now());

create table if not exists window_aggregate (
  id bigserial primary key, culto text not null, fonte text not null, t_ini real, t_fim real,
  quadros int, quadros_com_plateia int, n_total int, n_mensuravel int, insuficiente boolean not null,
  pct_voltados real, pct_sorrindo real, expressividade real, pct_olhos_fechados real, altura_mediana_px real,
  created_at timestamptz default now());
create index if not exists window_aggregate_culto on window_aggregate (culto, t_ini);

create table if not exists transcript_segment (id bigserial primary key, culto text not null, t_ini real, t_fim real, texto text);
create table if not exists moment (id bigserial primary key, culto text not null, nome text, t_ini real, t_fim real);
create table if not exists event (id bigserial primary key, culto text not null, tipo text, t_ini real, t_fim real, sinal text, magnitude_pp real, cobertura_min int, momento text);
create table if not exists insight (id bigserial primary key, culto text not null, minuto text, momento text, trecho text, texto text, sinais jsonb, evento text, revisado_por text, revisado_em timestamptz);
create table if not exists insight_feedback (id bigserial primary key, insight_id bigint references insight(id), avaliador text, nota int check (nota between 1 and 5), comentario text, created_at timestamptz default now());
create table if not exists run_log (id bigserial primary key, culto text, provider text, duracao_video_s int, janelas int, cobertura_pct real, eventos int, insights int, flavor text, segundos_total real, etapas jsonb, custo_usd real, custo_por_hora_de_video_usd real, tempo_por_hora_de_video_s real, created_at timestamptz default now());

-- Retenção (job agendado): agregados 12 meses, relatórios/insights 24 meses.
-- RLS e perfis (pastor, midia, dpo) entram no PBI-041/PBI-057.
