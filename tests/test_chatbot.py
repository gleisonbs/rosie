from unittest import TestCase

from rosie.chatbot import Chatbot
from rosie.nlp_engine import NLPEngine


class TestChatbot(TestCase):
    def setUp(self):
        self.chatbot = Chatbot(NLPEngine().pt, "test.name")

    def test_has_all_attributes(self):
        self.assertEqual(
            hasattr(self.chatbot, "intents"),
            True,
            "Chatbot: no intents attribute found",
        )
        self.assertEqual(
            hasattr(self.chatbot, "name"),
            True,
            "Chatbot: no name attribute found",
        )

    def test_can_initiate_correctly(self):
        self.assertEqual(
            self.chatbot.name,
            "test.name",
            "Chatbot: name attribute initialized incorrectly",
        )
        self.assertEqual(
            self.chatbot.intents,
            [],
            "Chatbot: intents attribute initialized incorrectly",
        )

    def test_has_add_intent_method(self):
        self.assertEqual(
            hasattr(self.chatbot, "add_intent"),
            True,
            "Chatbot: no add_intent method found",
        )
        add_intent = self.chatbot.add_intent
        self.assertEqual(
            hasattr(add_intent, "__call__"),
            True,
            "Chatbot: add_intent is not a method",
        )
        self.assertEqual(
            add_intent.__code__.co_argcount,
            1 + 2,
            "Chatbot: add_intent should accept two parameters (name, phrases)",
        )

    def test_has_get_intent_by_token_method(self):
        self.assertEqual(
            hasattr(self.chatbot, "get_intent_by_token"),
            True,
            "Chatbot: no get_intent_by_token method found",
        )
        get_intent_by_token = self.chatbot.get_intent_by_token
        self.assertEqual(
            hasattr(get_intent_by_token, "__call__"),
            True,
            "Chatbot: get_intent_by_token is not a method",
        )
        self.assertEqual(
            get_intent_by_token.__code__.co_argcount,
            1 + 1,
            "Chatbot: get_intent_by_token should accept"
            "two parameters (name, phrases)",
        )

    def test_correctly_adds_new_intent(self):
        intent_name = "test.intent"
        intent_phrases = ["test1", "test2", "test3"]
        self.assertEqual(
            len(self.chatbot.intents),
            0,
            "Chatbot: intents should be empty when initialized",
        )
        self.chatbot.add_intent(intent_name, intent_phrases)
        self.assertEqual(
            len(self.chatbot.intents),
            1,
            "Chatbot: add_intents failed to add to intents",
        )

    def test_correctly_returns_most_similar_intent(self):
        self.chatbot.add_intent(
            "price",
            ["qual o valor", "quanto custa", "preço", "me fala o total"],
        )
        self.chatbot.add_intent(
            "greet",
            [
                "oi",
                "olá",
                "tudo bem",
                "como vai",
                "opa",
                "bom dia",
                "boa noite",
                "boa tarde",
            ],
        )

        token = "quanto custa"
        name, value = self.chatbot.get_intent_by_token(token)
        self.assertEqual(
            name,
            "price",
            "Chatbot: get_intent_by_token failed to return correct intent",
        )
        self.assertEqual(
            value,
            1,
            "Chatbot: get_intent_by_token failed to return correct intent",
        )

        token = "oi, tudo bem?"
        name, value = self.chatbot.get_intent_by_token(token)
        self.assertEqual(
            name,
            "greet",
            "Chatbot: get_intent_by_token failed to return correct intent",
        )

    def test_prints_correctly(self):
        self.assertEqual(str(self.chatbot), "{}")

        self.chatbot.add_intent("test_intent1", ["test1", "test2", "test3"])
        self.chatbot.add_intent("test_intent2", ["test4", "test5", "test6"])

        expected_str = """intent:test_intent1
 - test1
 - test2
 - test3
intent:test_intent2
 - test4
 - test5
 - test6
"""
        self.assertEqual(
            str(self.chatbot),
            expected_str,
            "Chatbot: __str__ return incorrect formatted data",
        )
