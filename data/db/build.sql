CREATE TABLE IF NOT EXISTS guilds (
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "-"
);

CREATE TABLE IF NOT EXISTS userDATA (
    UserID integer PRIMARY KEY,
    wakaTime_UID text DEFAULT "no_user_set",
    APIKEY text DEFAULT "no_key_set",
    LastModified text DEFAULT CURRENT_TIMESTAMP
);