from typing import Optional

from CHRLINE_FIX import CHRLINE
from CHRLINE_FIX.services.thrift.ttypes import Message


class Messenger:
    def __init__(self, chrline: CHRLINE):
        self.chrline = chrline

    def isE2EE(self, msg: Message) -> bool:
        return getattr(msg, "isE2EE", False) or bool(msg.chunks)

    def sendMessage(
        self, got_msg: Message, text: str, file_path: Optional[str] = None
    ) -> None:
        to = got_msg.to
        is_e2ee = self.isE2EE(got_msg)

        if file_path:
            self._send_image(to, file_path, is_e2ee)
        else:
            self._send_text(to, text, is_e2ee)

    def _send_image(self, to: str, file_path: str, is_e2ee: bool) -> None:
        if is_e2ee:
            self.chrline.uploadMediaByE2EE(file_path, "image", to)
        else:
            self.chrline.sendImage(to, file_path)

    def _send_text(self, to: str, text: str, is_e2ee: bool) -> None:
        send_func = (
            self.chrline.sendCompactE2EEMessage
            if is_e2ee
            else self.chrline.sendCompactMessage
        )
        send_func(to, text)
