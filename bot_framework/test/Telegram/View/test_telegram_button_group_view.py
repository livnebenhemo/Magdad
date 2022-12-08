import unittest
from unittest.mock import MagicMock

from bot_framework.test.test_bot_user import TestBotUser
from telegram import InlineKeyboardMarkup

from bot_framework.session import Session
from bot_framework.Telegram.telegram_ui import TelegramUI
from bot_framework.Telegram.View.telegram_button_group_view import TelegramButtonGroupView
from bot_framework.test.mock_container import MockContainer



class TestTelegramButtonGroupView(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        bot = MockContainer()
        bot.send_photo = MagicMock()
        bot.send_message = MagicMock()
        bot.send_contact = MagicMock()

        dispatcher = MockContainer()
        dispatcher.add_handler = MagicMock()

        cls.ui = TelegramUI(bot, dispatcher, TestBotUser)
        cls.user = TestBotUser(telegram_id='id_test', id="123")
        cls.session = cls.ui.create_session("Testing", cls.user)

    def test_draw(self):
        buttons = [self.ui.create_button_view("b1", lambda s: None), self.ui.create_button_view("b2", lambda s: None)]
        view = TelegramButtonGroupView(self.session.view_container, "test", buttons)
        view.draw()

        args, kwargs = self.ui.raw_bot.send_message.call_args
        self.assertEqual(args[0], self.session)
        self.assertEqual(args[1], self.user.telegram_id)
        self.assertEqual(args[2], "test")

        got_buttons = kwargs['reply_markup']
        self.assertIsInstance(got_buttons, InlineKeyboardMarkup)
        self.assertEqual(len(got_buttons.inline_keyboard), 2)
        self.assertEqual(got_buttons.inline_keyboard[0][0].text, "b1")
        self.assertEqual(got_buttons.inline_keyboard[1][0].text, "b2")

    def test_update(self):
        buttons = [self.ui.create_button_view("b1", lambda s: None), self.ui.create_button_view("b2", lambda s: None)]
        view = TelegramButtonGroupView(self.session.view_container, "test", buttons)
        view.draw()

        view.raw_object.result().edit_text = MagicMock()
        buttons = [self.ui.create_button_view("u1", lambda s: None), self.ui.create_button_view("u2", lambda s: None), self.ui.create_button_view("u3", lambda s: None)]
        view.update("updated", buttons)

        args, kwargs = view.raw_object.result().edit_text.call_args
        self.assertEqual(args[0], "updated")

        got_buttons = kwargs['reply_markup']
        self.assertIsInstance(got_buttons, InlineKeyboardMarkup)
        self.assertEqual(len(got_buttons.inline_keyboard), 3)
        self.assertEqual(got_buttons.inline_keyboard[0][0].text, "u1")
        self.assertEqual(got_buttons.inline_keyboard[1][0].text, "u2")
        self.assertEqual(got_buttons.inline_keyboard[2][0].text, "u3")

    def test_delete(self):
        buttons = [self.ui.create_button_view("b1", lambda s: None), self.ui.create_button_view("b2", lambda s: None)]
        view = TelegramButtonGroupView(self.session.view_container, "test", buttons)
        view.draw()

        view.raw_object.result().delete = MagicMock()
        temp = view.raw_object
        view.remove()
        temp.result().delete.assert_called_with()
