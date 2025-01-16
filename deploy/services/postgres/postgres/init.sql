create table if not exists users
(
    player_id  char(13) not null,
    mod_name   char(30) not null,
    users_data jsonb,
    primary key (player_id, mod_name)
);

create table if not exists inventory
(
    player_id      char(13) not null,
    mod_name       char(30) not null,
    inventory_data jsonb,
    foreign key (player_id, mod_name) references users (player_id, mod_name),
    primary key (player_id, mod_name)
);

create table if not exists decks
(
    player_id char(13) not null,
    mod_name  char(30) not null,
    deck_id   char(36) not null,
    deck_data jsonb,
    foreign key (player_id, mod_name) references users (player_id, mod_name),
    primary key (player_id, mod_name, deck_id)
);