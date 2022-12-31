import sqlite3

db = sqlite3.connect('bot_data.sqlite')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS user_data (
	id INT,
	chat_id_to_posts TEXT,
	channel_id_to_posts TEXT
	)""")
db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS channels_data (
	channel_name TEXT,
	last_post TEXT
	)""")
db.commit()

sql.execute(f"INSERT INTO user_data VALUES (?, ?, ?)", (1, '0', '1'))
db.commit()

sql.execute(f"INSERT INTO channels_data VALUES (?, ?)", ('telegram', '0'))
db.commit()