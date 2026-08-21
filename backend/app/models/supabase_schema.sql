-- ============================================================
-- CREATORS TABLE
-- ============================================================

create table if not exists public.creators (

    id bigint generated always as identity primary key,

    username text not null unique,

    name text,

    contact_email text,

    follower_count bigint,

    profile_url text,

    verified boolean default false,

    bio text,

    engagement_rate numeric(10, 2),

    category text,

    content_themes jsonb default '[]'::jsonb,

    created_at timestamptz
        not null
        default now(),

    updated_at timestamptz
        not null
        default now()
);


-- ============================================================
-- REELS TABLE
-- ============================================================

create table if not exists public.reels (

    id bigint generated always as identity primary key,

    creator_id bigint not null,

    instagram_url text not null,

    description text,

    likes bigint default 0,

    comments bigint default 0,

    scraped_at timestamptz
        not null
        default now(),

    constraint fk_reels_creator
        foreign key (creator_id)
        references public.creators(id)
        on delete cascade,

    constraint unique_creator_reel
        unique (creator_id, instagram_url)
);


-- ============================================================
-- INDEXES
-- ============================================================

create index if not exists idx_creators_username
on public.creators(username);

create index if not exists idx_reels_creator_id
on public.reels(creator_id);


-- ============================================================
-- UPDATED_AT FUNCTION
-- ============================================================

create or replace function public.update_updated_at_column()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;


-- ============================================================
-- UPDATED_AT TRIGGER
-- ============================================================

drop trigger if exists update_creators_updated_at
on public.creators;

create trigger update_creators_updated_at

before update
on public.creators

for each row

execute function public.update_updated_at_column();