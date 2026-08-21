-- ============================================================
-- OUTREACH TABLE
-- ============================================================

create table if not exists public.outreach (

    id bigint generated always as identity primary key,

    creator_id bigint not null,

    -- ========================================================
    -- EMAIL
    -- ========================================================

    email_subject text,

    email_body text,

    email_status text
        not null
        default 'pending',

    email_sent_at timestamptz,

    -- ========================================================
    -- INSTAGRAM DM
    -- ========================================================

    instagram_dm text,

    instagram_dm_status text
        not null
        default 'pending',

    instagram_dm_sent_at timestamptz,

    -- ========================================================
    -- COMMON
    -- ========================================================

    generated_at timestamptz
        not null
        default now(),

    updated_at timestamptz
        not null
        default now(),

    -- ========================================================
    -- FOREIGN KEY
    -- ========================================================

    constraint fk_outreach_creator

        foreign key (creator_id)

        references public.creators(id)

        on delete cascade,

    -- ========================================================
    -- ONE OUTREACH RECORD PER CREATOR
    -- ========================================================

    constraint unique_outreach_creator

        unique (creator_id)
);


-- ============================================================
-- INDEX
-- ============================================================

create index if not exists idx_outreach_creator_id

on public.outreach(creator_id);


-- ============================================================
-- UPDATED_AT FUNCTION
-- ============================================================

create or replace function public.update_outreach_updated_at()

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

drop trigger if exists update_outreach_updated_at

on public.outreach;


create trigger update_outreach_updated_at

before update

on public.outreach

for each row

execute function public.update_outreach_updated_at();