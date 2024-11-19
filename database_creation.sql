set foreign_key_checks = 0;

CREATE TABLE IF NOT EXISTS `game`(
    game_id int primary key not null auto_increment,
    name varchar(64),
    password varchar(64),
    starting_airport varchar(16),
    location varchar(16),
    money int,
    fuel float,
    fuel_used float,
    lootboxes_opened int,
    flights_taken int,
    diamond bool,

    foreign key (starting_airport) references airport(ident),
    foreign key (location) references airport(ident)
);

CREATE TABLE IF NOT EXISTS `game_airports`(
    id int primary key not null auto_increment,
    game_id int,
    airport_id varchar(16),
    lootbox_status bool,
    lootbox_id int,

    foreign key (game_id) references game(game_id),
    foreign key (airport_id) references airport(ident),
    foreign key (lootbox_id) references goals(id)

);

CREATE TABLE IF NOT EXISTS `goals`(
    id int primary key not null auto_increment,
    reward int,
    rarity varchar(64),
    goal_name varchar(64),
    UNIQUE(reward, rarity, goal_name)
);

INSERT IGNORE INTO `goals` (reward,rarity, goal_name) VALUES
    (300, "Common", "Topaz"),
    (600, "Rare", "Emerald"),
    (1000, "Epic", "Ruby"),
    (0, "Very common", "Milk"),
    (-1, "Very rare", "Robber"),
    (1, "Legendary", "Diamond");
set foreign_key_checks = 1;