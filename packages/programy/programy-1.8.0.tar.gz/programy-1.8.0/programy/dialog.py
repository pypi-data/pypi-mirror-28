"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import os
import time
from os import listdir
from os.path import isfile, join


class Sentence(object):

    def __init__(self, text: str = None, split_chars: str = " "):
        self._words = self._split_into_words(text, split_chars)
        self._response = None
        self._matched_context = None

    @property
    def words(self):
        return self._words

    def append_word(self, word):
        self._words.append(word)

    def append_sentence(self, sentence):
        for word in sentence.words:
            self._words.append(word)

    def replace_words(self, text):
        self._words = self._split_into_words(text, " ")

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, text: str):
        self._response = text

    @property
    def matched_context(self):
        return self._matched_context

    @matched_context.setter
    def matched_context(self, context):
        self._matched_context = context

    def num_words(self):
        return len(self.words)

    def word(self, num: int):
        if num < self.num_words():
            return self.words[num]
        return None

    def words_from_current_pos(self, current_pos: int):
        if self._words:
            return " ".join(self._words[current_pos:])
        raise Exception("Num word array violation !")

    def text(self):
        return " ".join(self._words)

    def _split_into_words(self, sentence, split_chars: str):
        if sentence is None:
            return []
        else:
            sentence = sentence.strip()
            if not sentence:
                return []
            return sentence.split(split_chars)


class Question(object):

    @staticmethod
    def create_from_text(text: str, sentence_split_chars: str = ".", word_split_chars: str = " ", split=True):
        question = Question()
        if split is True:
            question.split_into_sentences(text, sentence_split_chars, word_split_chars)
        else:
            question.sentences.append(Sentence(text))
        return question

    @staticmethod
    def create_from_sentence(sentence: Sentence):
        question = Question()
        question.sentences.append(sentence)
        return question

    @staticmethod
    def create_from_question(question):
        new_question = Question()
        for each_sentence in question.sentences:
            new_question.sentences.append(each_sentence)
        return new_question

    def __init__(self):
        self._sentences = []
        self._properties = {}
        self._current_sentence_no = -1

    @property
    def sentences(self):
        return self._sentences

    def set_current_sentence_no(self, sentence_no):
        self._current_sentence_no = sentence_no

    def set_property(self, name: str, value: str):
        self._properties[name] = value

    def property(self, name: str):
        if name in self._properties:
            return self._properties[name]
        return None

    def sentence(self, num: int):
        if num < len(self._sentences):
            return self._sentences[num]
        raise Exception("Num sentence array violation !")

    def current_sentence(self):
        if not self._sentences:
            raise Exception("Num sentence array violation !")
        return self._sentences[self._current_sentence_no]

    def previous_nth_sentence(self, num):
        if len(self._sentences) < num:
            raise Exception("Num sentence array violation !")
        previous = -1 - num
        return self._sentences[previous]

    def combine_sentences(self):
        return ". ".join([sentence.text() for sentence in self._sentences])

    def combine_answers(self):
        return ". ".join([sentence.response for sentence in self.sentences if sentence.response is not None])

    def split_into_sentences(self, text: str, sentence_split_chars: str, word_split_chars: str):
        if text is not None and text.strip():
            self._sentences = []
            all_sentences = text.split(sentence_split_chars)
            for each_sentence in all_sentences:
                self._sentences.append(Sentence(each_sentence, word_split_chars))
#
# A Conversation is made up of questions, each question is made up of sentences
#
class Conversation(object):

    def __init__(self, clientid: str, bot: object):
        self._bot = bot
        self._clientid = clientid
        self._questions = []
        self._max_histories = bot.configuration.conversations.max_histories
        self._properties = {}
        self._properties['topic'] = bot.configuration.conversations.initial_topic

    @property
    def bot(self):
        return self._bot

    @property
    def clientid(self):
        return self._clientid

    @property
    def questions(self):
        return self._questions

    @property
    def max_histories(self):
        return self._max_histories

    @property
    def properties(self):
        return self._properties

    def has_current_question(self):
        return bool(self._questions)

    def current_question(self):
        if self._questions:
            return self._questions[-1]
        raise Exception("Invalid question index")

    def previous_nth_question(self, num: int):
        if len(self._questions) < num:
            raise Exception("Num question array violation !")
        previous = -1 - num
        return self._questions[previous]

    def set_property(self, name: str, value: str):
        if name == 'topic':
            if value == "":
                value = '*'

        self._properties[name] = value

    def property(self, name: str):
        if self._properties is not None:
            if name in self._properties:
                return self._properties[name]
        return None

    def record_dialog(self, question: Question):
        if len(self._questions) == self._max_histories:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Conversation history at max [%d], removing oldest", self._max_histories)
            self._questions.remove(self._questions[0])
        self._questions.append(question)

    def pop_dialog(self):
        if self._questions:
            self._questions.pop()

    def load_initial_variables(self, variables_collection):
        for pair in variables_collection.pairs:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("Setting variable [%s] = [%s]", pair[0], pair[1])
            self._properties[pair[0]] = pair[1]


class ConversationFileStorage(object):

    def __init__(self, config):
        self._config = config
        self._last_modified = None

    def empty(self):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Emptying Conversation Folder")
        try:
            if self._config._dir is not None:
                if os.path.exists(self._config._dir):
                    convo_files = [f for f in listdir(self._config._dir) if isfile(join(self._config._dir, f))]
                    for file in convo_files:
                        fullpath = self._config._dir + os.sep + file
                        if logging.getLogger().isEnabledFor(logging.DEBUG):
                            logging.debug("Removing conversation file: [%s]"%fullpath)
                        os.remove(fullpath)
        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed emptying conversation directory [%s]"%self._config._dir)
                logging.exception(e)

    def save_conversation(self, conversation, clientid):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Saving conversation")
        try:
            if self._config._dir is not None:
                if os.path.exists(self._config._dir):
                    filename = self._config._dir + os.sep + clientid + ".convo"
                    with open(filename, "w+", encoding="utf-8") as convo_file:
                        for name, value in conversation._properties.items():
                            convo_file.write("%s:%s\n"%(name, value))
                        convo_file.write("\n")
        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed to save conversation for clientid [%s]"%clientid)
                logging.exception(e)

    def load_conversation(self, conversation, clientid, restore_last_topic=False):
        try:
            if self._config._dir is not None:
                if os.path.exists(self._config._dir):
                    filename = self._config._dir + os.sep + clientid + ".convo"
                    if os.path.exists(filename):

                        should_open = True
                        last_modified = time.ctime(os.path.getmtime(filename))
                        if self._last_modified is not None:
                            if self._last_modified >= last_modified:
                                should_open = False
                        self._last_modified = last_modified

                        if should_open is True:
                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                logging.debug("Loading Conversation")

                            with open(filename, "r", encoding="utf-8") as convo_file:
                                for line in convo_file:
                                    if ':' in line:
                                        splits = line.split(":")
                                        name = splits[0].strip()
                                        value = splits[1].strip()
                                        if name == "topic":
                                            if restore_last_topic is True:
                                                if logging.getLogger().isEnabledFor(logging.DEBUG):
                                                    logging.debug("Loading stored property [%s]=[%s] for %s" % (name, value, clientid))
                                                conversation._properties[name] = value
                                        else:
                                            if logging.getLogger().isEnabledFor(logging.DEBUG):
                                                logging.debug("Loading stored property [%s]=[%s] for %s" % (name, value, clientid))
                                            conversation._properties[name] = value

        except Exception as e:
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Failed to load conversation for clientid [%s]"%clientid)
                logging.exception(e)

