import sqlite3

class BotDB:
	def __init__(self, db_file):
		"""Иницилизация соединения с БД"""
		print('Иницилизация соединения с БД')
		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()

	def user_exists(self, user_id):
		"""Проверяем, есть ли user в DB"""
		result = self.cursor.execute(f"SELECT id FROM users_data WHERE id = ?", (user_id,))
		return bool(len(result.fetchall()))

	def add_user(self, user_id, user_name):
		"""Добавить юзера"""
		self.cursor.execute(f"INSERT INTO users_data VALUES (?, ?, ?, ?)", (user_id, user_name, 0, 3))
		return self.conn.commit()

	def add_record(self, user_id, operation, value):
		"""Создать надпись о расходе/доходе"""
		self.cursor.execute(f"INSERT INTO records (id, operation, value) VALUES (?, ?, ?)",
			(self.get_user_id(user_id),
				operation == '+',
				value))
		return self.conn.commit()

	def how_many_channels(self, table):
		result = self.cursor.execute(f'SELECT COUNT(channel_name) FROM {table}')
		return result.fetchone()[0]

	def add_channel_to_repost(self, channel):
		print('канал добавлен')
		self.cursor.execute(f"INSERT INTO channels_data VALUES (?, ?)", (channel,'0'))
		return self.conn.commit()

	def channels_exist(self, channel):
		result = self.cursor.execute('SELECT channel_name FROM channels_data WHERE channel_name=?', (channel,)).fetchone()
		print(f'result: {result}')
		print(f'type result: {type(result)}')
		try:
			if len(result) == 0:
				return False
			else:
				return True
		except:
			if result == None:
				return False
			else:
				return True


	def remove_channel_to_repost(self, channel):
		self.cursor.execute(f'DELETE FROM channels_data WHERE channel_name=?', (channel,))
		return self.conn.commit()
	
	def set_channel_to_repost(self, channel_name):
		self.cursor.execute(f'UPDATE user_data SET channel_id_to_posts = ? WHERE id = 1', (channel_name,))
		return self.conn.commit()

	def set_chat_to_repost(self, chat_name):
		self.cursor.execute(f'UPDATE user_data SET chat_id_to_posts = ? WHERE id = 1', (chat_name,))
		return self.conn.commit()
	
	def get_chat_to_repost(self):
		result = self.cursor.execute(f'SELECT chat_id_to_posts FROM user_data WHERE id = 1')
		return result.fetchone()[0]
	
	def get_channel_to_repost(self):
		result = self.cursor.execute(f'SELECT channel_id_to_posts FROM user_data WHERE id = 1')
		return result.fetchone()[0]

	def get_channels(self):
		channels = []
		result = self.cursor.execute(f'SELECT channel_name FROM channels_data').fetchall()
		for i in result:
			channels.append(i[0])
		return channels

	def close(self):
		self.conn.close()