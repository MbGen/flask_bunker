DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS open_stats;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE room (
    id INTEGER UNIQUE PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    creator INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES user (id),
    FOREIGN KEY (creator) REFERENCES user (id)
);

CREATE TABLE game (
    id INTEGER,
    player_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (id) REFERENCES room (id),
    FOREIGN KEY (player_id) REFERENCES user (id)
);

CREATE TABLE open_stats (
    room_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    profession BOOLEAN,
    biology BOOLEAN,
    health BOOLEAN,
    hobby BOOLEAN,
    baggage BOOLEAN,
    facts BOOLEAN,
    special_cards BOOLEAN,
    disaster BOOLEAN,
    FOREIGN KEY (room_id) REFERENCES room (id),
    FOREIGN KEY (player_id) REFERENCES user (id)
);
