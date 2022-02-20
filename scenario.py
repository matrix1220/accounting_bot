
from config import bot

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.objects import Message
from photon import key, act, explicit_act, back

#from photon.methods import sendMessage

from dbscheme import Action, Tag, ActionTag
from sqlalchemy import func


class ActionMenu(OutlineMenu):
	keyboard = [
		[ ("Back", back()) ],
	]
	async def _act(self):
		self.register()
		return await getattr(self, f"act_{len(self.args)}")()

	async def act_0(self):
		return Message('Input amount:')

	async def act_1(self):
		return Message('Input tags:')

	async def act_2(self):
		amount, tags = self.args
		db = self.context.db
		user_id = self.context.user.id
		action_id, = db.query(func.max(Action.id)).filter_by(user_id=user_id).first()
		action_id = action_id + 1 if action_id else 1
		action = Action(
			user_id=user_id,
			id=action_id,
			amount=amount,
		)
		db.add(action)
		for tag in tags.split(' '):
			tag_ = db.query(Tag).filter_by(name=tag).first()
			if not tag_:
				tag_id, = db.query(func.max(Tag.id)).filter_by(user_id=user_id).first()
				tag_id = tag_id + 1 if tag_id else 1
				tag_ = Tag(user_id=user_id, id=tag_id, name=tag)
				db.add(tag_)
			else:
				tag_id = tag_.id
			db.add(ActionTag(user_id=user_id, action_id=action_id, tag_id=tag_id))

		await self.exec(Message('Done'))
		return await self.context.back()

	async def handle_text(self, text):
		return await self.context.explicit_act(ActionMenu, *self.args, text)

class CalculateMenu(OutlineMenu):
	keyboard = [
		[ ("All", key("all")) ],
		[ ("Back", back()) ],
	]
	async def _act(self):
		self.register()
		return Message('Input tags you want to calculate:')

	async def handle_key_all(self):
		db = self.context.db
		actions = db.query(Action)

		text = 'Result:\n'
		total = 0
		for action in actions:
			text += f"{action.amount} {','.join([action_tag.name for action_tag in action.tags])}\n"
			total += action.amount

		text += f"Total: {total}\n"
		return Message(text)

	async def handle_text(self, text):
		db = self.context.db
		tag_ids = db.query(Tag.id).filter(Tag.name.in_(text.split(' '))).cte()
		actions = db.query(Action, ActionTag)\
			.filter(Action.id==ActionTag.action_id)\
			.filter(ActionTag.tag_id.in_(tag_ids))

		text = 'Result:\n'
		total = 0
		for action, action_tag in actions:
			text += f"{action.amount}\n"
			total += action.amount

		text += f"Total: {total}\n"
		return Message(text)

@bot.set_main_menu
class MainMenu(OutlineMenu):
	keyboard = [
		[ ("Action", act(ActionMenu) ) ],
		[ ("Calculate", act(CalculateMenu)) ],
	]
	async def _act(self, arg=None):
		self.register()
		return Message('Main Menu')