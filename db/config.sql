-- =============================================================================
-- 1. Create the Extensions Schema and Vector Extension
-- =============================================================================

-- Create the "extensions" schema for the vector extension and grant usage
create schema if not exists extensions;
grant usage on schema extensions to public;

-- Create the vector extension in the "extensions" schema
create extension if not exists vector schema extensions;

-- Set the search_path so that objects are created in public and extensions
alter database postgres set search_path = public, extensions;


-- =============================================================================
-- 2. Create Tables, Functions, and Triggers in Public
-- =============================================================================

-- Create the admin_users table in public
create table if not exists public.admin_users (
    user_id uuid primary key references auth.users(id) on delete cascade,
    is_admin boolean default false,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create a trigger function to add a new admin user entry when a new user is inserted
create or replace function public.create_admin_user_entry()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
    insert into public.admin_users (user_id, is_admin)
    values (new.id, false);
    return new;
end;
$$;

-- Create trigger on auth.users to call the above function on insert
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row
    execute function public.create_admin_user_entry();

-- Create a function to check if the current user is an admin
create or replace function public.is_admin()
returns boolean
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
    return (
        select is_admin
        from public.admin_users
        where user_id = auth.uid()
    );
end;
$$;

-- Create an enum type for document statuses in public
create type public.document_status as enum ('processing', 'completed', 'error');

-- Create the documents table in public
create table if not exists public.documents (
    id uuid default gen_random_uuid() primary key,
    uploaded_by uuid references auth.users(id) on delete cascade,
    filename text not null,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    status public.document_status default 'processing',
    error_message text
);

-- Create the document_chunks table in public
create table if not exists public.document_chunks (
    id uuid default gen_random_uuid() primary key,
    document_id uuid references public.documents(id) on delete cascade,
    chunk_index integer not null,
    content text not null,
    embedding extensions.vector(384),
    created_at timestamp with time zone default now()
);

-- Create an index on the document_chunks.embedding column for fast vector searches
create index if not exists document_chunks_embedding_idx
    on public.document_chunks using ivfflat (embedding extensions.vector_cosine_ops)
    with (lists = 100);

-- Create a trigger function to update the updated_at column
create or replace function public.update_updated_at_column()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

-- Create a trigger to update documents.updated_at on update
drop trigger if exists update_documents_updated_at on public.documents;
create trigger update_documents_updated_at
    before update on public.documents
    for each row
    execute function public.update_updated_at_column();

-- Create a trigger to update admin_users.updated_at on update
drop trigger if exists update_admin_users_updated_at on public.admin_users;
create trigger update_admin_users_updated_at
    before update on public.admin_users
    for each row
    execute function public.update_updated_at_column();


-- =============================================================================
-- 3. Enable Row-Level Security (RLS) and Define Policies in Public
-- =============================================================================

-- Enable RLS on the tables
alter table public.documents enable row level security;
alter table public.document_chunks enable row level security;
alter table public.admin_users enable row level security;

-- Documents policies
create policy "Everyone can view documents"
    on public.documents for select
    to authenticated
    using (true);

create policy "Only admins can insert documents"
    on public.documents for insert
    to authenticated
    with check (public.is_admin());

create policy "Only admins can update documents"
    on public.documents for update
    to authenticated
    using (public.is_admin());

create policy "Only admins can delete documents"
    on public.documents for delete
    to authenticated
    using (public.is_admin());

-- Document chunks policies
create policy "Everyone can view document chunks"
    on public.document_chunks for select
    to authenticated
    using (true);

create policy "Only admins can modify document chunks"
    on public.document_chunks for all
    to authenticated
    using (public.is_admin());

-- Admin users policies
create policy "Admins can view admin_users"
    on public.admin_users for select
    to authenticated
    using (public.is_admin());

create policy "Admins can update admin_users"
    on public.admin_users for update
    to authenticated
    using (public.is_admin());


-- =============================================================================
-- 4. Create Helper Functions and RPCs in Public
-- =============================================================================

-- Function to set admin status (only callable by admins)
create or replace function public.set_admin_status(
    target_user_id uuid,
    admin_status boolean
)
returns void
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
    if not public.is_admin() then
        raise exception 'Only admins can modify admin status';
    end if;

    update public.admin_users
    set is_admin = admin_status
    where user_id = target_user_id;
end;
$$;

-- Search function to query document chunks based on vector similarity
create or replace function public.search_documents(
    query_embedding extensions.vector(768),
    match_threshold float default 0.7,
    match_count int default 5
)
returns table (
    id uuid,
    content text,
    document_id uuid,
    filename text,
    similarity float
)
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
    return query
    select
        dc.id,
        dc.content,
        dc.document_id,
        d.filename,
        1 - (dc.embedding <=> query_embedding) as similarity
    from public.document_chunks dc
    join public.documents d on d.id = dc.document_id
    where 1 - (dc.embedding <=> query_embedding) > match_threshold
    order by dc.embedding <=> query_embedding
    limit match_count;
end;
$$;


-- =============================================================================
-- 5. Grant Permissions on Public Objects
-- =============================================================================

grant select, insert, update, delete on public.admin_users to authenticated, anon;
grant select, insert, update, delete on public.documents to authenticated, anon;
grant select, insert, update, delete on public.document_chunks to authenticated, anon;

GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;
