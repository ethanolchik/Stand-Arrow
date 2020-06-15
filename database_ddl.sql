CREATE TABLE stand (
    stand_id serial PRIMARY KEY,
    stand_name varchar(40) NOT NULL,
    stand_description text,
    CONSTRAINT name UNIQUE(stand_name)
);
CREATE TABLE player (
    player_id serial PRIMARY KEY,
    player_name varchar(40) NOT NULL,
    CONSTRAINT player_name UNIQUE(player_name)
);

CREATE Table item (
    item_id serial PRIMARY KEY,
    item_name varchar(40) NOT NULL,
    item_description text,
    CONSTRAINT name UNIQUE(item_name)
);

Create Table user_item (
    player_id int REFERENCES player (player_id) ON UPDATE CASCADE ON DELETE CASCADE,
    item_id int REFERENCES item (item_id) ON UPDATE CASCADE ON DELETE CASCADE,
    amount numeric NOT NULL DEFAULT 1,
    CONSTRAINT user_item_pkey PRIMARY KEY (player_id, item_id)
);

/*

user_id, user_name, item_name, amt

------------------
1, Bob, Pencils, 5
1, Bob, Erasers, 1
------------------

SELECT user.user_id, user.user_name, item.item_name, user_item.amt
FROM user
LEFT OUTER JOIN user_item ON (user_item.user_id = user.user_id)
INNER JOIN item ON (item.item_id = user_item.item_id)
WHERE user.user_id = 1

*/
