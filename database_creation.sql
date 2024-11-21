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
    diamond int,

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

CREATE TABLE IF NOT EXISTS `lootboxes`(
    id int primary key not null auto_increment,
    reward int,
    rarity varchar(64),
    spawn_weight int(64),
    goal_name varchar(64),
    UNIQUE(reward, rarity, spawn_weight, goal_name)
);

INSERT IGNORE INTO `lootboxes` (reward,rarity,spawn_weight, goal_name) VALUES
    (300, "Common", 10, "Topaz"),
    (600, "Rare",7 , "Emerald"),
    (1000, "Epic" ,5, "Ruby"),
    (0, "Very common",15 , "Milk"),
    (-1, "Very rare",2 , "Robber"),
    (1, "Legendary",1 , "Diamond");
set foreign_key_checks = 1;