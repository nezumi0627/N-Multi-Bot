# -*- coding: utf-8 -*-

# last update: 2024/08/29 2:24

import json
import logging
import re
import time
import timeit
from functools import wraps
from typing import Callable, Dict

from CHRLINE_FIX import CHRLINE
from messenger import Messenger


class CommandHandler:
    def __init__(self, chrline: CHRLINE, messenger: Messenger, prefix: str):
        self.chrline = chrline
        self.messenger = messenger
        self.prefix = prefix
        self.command_handlers: Dict[str, Callable] = self.register_commands()

    def register_commands(self) -> Dict[str, Callable]:
        return {
            f"{self.prefix}{cmd}": getattr(self, f"command_{cmd}")
            for cmd in ["help", "speed", "time", "me", "mid", "gid", "userinfo"]
        }

    def generate_help_message(self) -> str:
        return "\n".join(
            f"{cmd} - {func.__doc__.strip() if func.__doc__ else '説明がありません。'}"
            for cmd, func in self.command_handlers.items()
        )

    def send_message_with_e2ee(self, func):
        """Send Message with E2EE Decorator"""

        @wraps(func)
        def wrapper(msg, *args, **kwargs):
            try:
                result = func(msg, *args, **kwargs)
                text, content_metadata = (
                    result if isinstance(result, tuple) else (result, None)
                )
                self.messenger.sendMessage(msg, text, content_metadata)
            except Exception as e:
                logging.error(f"Failed to send message: {e}")

        return wrapper

    @send_message_with_e2ee
    def command_help(self, msg) -> str:
        """Send Help Message"""
        return self.generate_help_message()

    @send_message_with_e2ee
    def command_speed(self, msg) -> str:
        """Send Speed Test Message"""
        speed = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
        return f"SpeedTest: {speed} s"

    @send_message_with_e2ee
    def command_time(self, msg) -> str:
        """Send Current Time Message"""
        stime = self.chrline.getServerTime()
        current_time = time.strftime(
            "%Y-%m-%d %I:%M:%S %p", time.localtime(stime / 1000)
        )
        return f"time: {current_time}"

    @send_message_with_e2ee
    def command_me(self, msg) -> str:
        """Send My Info Message"""
        try:
            self.chrline.sendContact(msg.to, msg._from, "github.com/nezumi0627")
        except Exception as e:
            return f"Error sending contact: {e}"

    @send_message_with_e2ee
    def command_mid(self, msg) -> str:
        """Send Mid Info Message"""
        mentionees = self.chrline.getMentioneesByMsgData(msg)
        if not mentionees:
            return msg._from

        reply = "\n".join(
            f"@{self.chrline.getContact(mid).displayName} {mid}" for mid in mentionees
        )
        mentions = [
            {"S": s, "L": len(line), "M": mid}
            for s, (line, mid) in enumerate(zip(reply.split("\n"), mentionees))
        ]
        return reply, self.chrline.genMentionData(mentions)

    @send_message_with_e2ee
    def command_userinfo(self, msg, text: str) -> str:
        """Send User Info Message"""
        user_mids = self.chrline.getMentioneesByMsgData(msg) or re.findall(
            r"(?<![a-f0-9])u[a-f0-9]{32}(?![a-f0-9])", text[10:]
        )
        for user_mid in user_mids:
            try:
                user = self.chrline.getContact(user_mid)
                return (
                    f"User Name:\n{user.displayname}\n"
                    f"User Mid:\n{user.mid}\n"
                    f"Status Message:\n(Only show 100 words!)\n{user.statusMessage[:100]}\n"
                    f"Profile Link:\n{self.chrline.LINE_PROFILE_CDN_DOMAIN}/{user.pictureStatus}"
                )
            except Exception as e:
                return f"Error fetching user info: {e}"

    @send_message_with_e2ee
    def command_gid(self, msg) -> str:
        """Send Group ID Message"""
        return msg.to

    def setup_e2ee_key(self) -> None:
        """Setup E2EE Key"""
        try:
            self.chrline.getE2EESelfKeyData(self.chrline.mid)
        except Exception as e:
            logging.error(f"Error retrieving E2EE key: {e}")
            self.chrline.registerE2EESelfKey()

    def load_database(self) -> None:
        """Load Settings from Database"""
        try:
            with open("./data/auther.json", "r", encoding="utf-8") as db_file:
                db = json.load(db_file)
                self.chrline.admin = set(db.get("admin", []))
                self.chrline.owner = set(db.get("owner", []))
        except FileNotFoundError:
            logging.error("Database file not found.")


class MessageProcessor:
    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def handle_message(self, op) -> None:
        """Process Message"""
        if not self._is_valid_message(op):
            return

        msg = op.message
        if (
            msg._from
            not in self.command_handler.chrline.owner
            | self.command_handler.chrline.admin
        ):
            return

        text = self._get_message_text(msg)

        if text.startswith("/userinfo:"):
            self.command_handler.command_userinfo(msg, text)
        elif handler := self.command_handler.command_handlers.get(text):
            handler(msg)

    def _is_valid_message(self, op) -> bool:
        return op.type == 25 and op.message.contentType == 0 and op.message.toType == 2

    def _get_message_text(self, msg) -> str:
        return (
            self.command_handler.chrline.decryptE2EETextMessage(msg)
            if msg.contentMetadata.get("e2eeVersion")
            else msg.text
        )


def main() -> None:
    """Main Function"""
    # Create Instances
    cl = CHRLINE(device="DESKTOPWIN", use_thrift=True)
    messenger = Messenger(cl)

    # Create CommandHandler Instance
    command_handler = CommandHandler(cl, messenger, "!")

    # Initial Setup
    command_handler.load_database()
    command_handler.setup_e2ee_key()

    # Create MessageProcessor Instance
    message_processor = MessageProcessor(command_handler)

    # Start Message Trace
    cl.trace(message_processor.handle_message)


if __name__ == "__main__":
    main()
