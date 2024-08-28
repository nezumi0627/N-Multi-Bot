from functools import partial
from typing import Callable, Optional

from CHRLINE_FIX import CHRLINE
from CHRLINE_FIX.services.thrift.ttypes import Message


class Messenger:
    def __init__(self, chrline: CHRLINE):
        self.chrline = chrline

    @staticmethod
    def is_e2ee(msg: Message) -> bool:
        return getattr(msg, "isE2EE", False) or bool(msg.chunks)

    def send_message(
        self, got_msg: Message, text: str, content_metadata: Optional[dict] = None
    ) -> None:
        to = got_msg.to
        is_e2ee = self.is_e2ee(got_msg)

        if content_metadata and content_metadata.get("ATTR_CONTENT_TYPE") == "image":
            self._send_media(to, text, is_e2ee, "image")
        else:
            self._send_text(to, text, is_e2ee)

    def _send_media(
        self, to: str, file_path: str, is_e2ee: bool, media_type: str
    ) -> None:
        send_func = self._get_send_func(is_e2ee, media_type)
        send_func(to, file_path)

    def _send_text(self, to: str, text: str, is_e2ee: bool) -> None:
        send_func = self._get_send_func(is_e2ee, "text")
        send_func(to, text)

    def _get_send_func(self, is_e2ee: bool, content_type: str) -> Callable:
        func_map = {
            ("image", True): partial(
                self.chrline.uploadMediaByE2EE, media_type="image"
            ),
            ("image", False): self.chrline.sendImage,
            ("text", True): self.chrline.sendCompactE2EEMessage,
            ("text", False): self.chrline.sendCompactMessage,
        }
        return func_map.get((content_type, is_e2ee))
