
from config import sessionmaker

from dbscheme import User, Message

from photon import ContextManager as ContextManager_
from photon import Context as Context_
from photon import OutlineMenuContext as OutlineMenuContext_
from photon import InlineMenuContext as InlineMenuContext_

from photon import MenuStack

class InlineMenuContext(InlineMenuContext_):
	def set_message_id(self, message_id):
		self.message.message_id = self.metadata['message_id']
		self.db.add(self.message)
		#self.db.commit()

	def commit(self):
		super().commit()
		self.db.commit()

class OutlineMenuContext(OutlineMenuContext_):
	def commit(self):
		super().commit()
		self.db.commit()

#db.commit()
class ContextManager(ContextManager_):
	def find_inline(self, metadata):
		db = sessionmaker()
		chat_id = metadata['chat_id']

		if metadata['message_id']:
			message = db.query(Message).filter_by(
				chat_id=chat_id,
				message_id=metadata['message_id'],
			).first()
		else:
			message = None

		if not message:
			message = Message(
				chat_id=chat_id,
				message_id=metadata['message_id'],
			)
			if metadata['message_id']:
				db.add(message)
				#db.commit()
			
		context = self.instantiate(InlineMenuContext, metadata)
		context.db = db
		context.message = message
		context.menu_stack = MenuStack(message.menu_stack)
		context.keyboard = message.keyboard

		return context

	def find_outline(self, metadata):
		db = sessionmaker()
		chat_id = metadata['chat_id']

		user = db.query(User).filter_by(id=chat_id).first()
		if not user:
			user = User(id=chat_id)
			db.add(user)			
			#db.commit()

		context = self.instantiate(OutlineMenuContext, metadata)
		context.db = db
		context.user = user
		context.menu_stack = MenuStack(user.menu_stack)
		context.keyboard = user.keyboard

		return context