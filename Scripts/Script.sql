CREATE TABLE word_search_puzzle(
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT NOT NULL
);
CREATE TABLE word_search_puzzle_list (
    id INTEGER PRIMARY KEY,
    puzzle_id INTEGER NOT NULL,
    word TEXT NOT NULL,
    FOREIGN KEY (puzzle_id)
        REFERENCES word_search_puzzle(id)
        ON DELETE CASCADE
);

CREATE TABLE users (
	id TEXT PRIMARY KEY,
	password TEXT PRIMARY KEY
)