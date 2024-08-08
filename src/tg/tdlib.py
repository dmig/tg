from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from telegram.client import AsyncResult, Telegram


class ChatAction(Enum):
    chatActionTyping = "typing"  # noqa: N815
    chatActionCancel = "cancel"  # noqa: N815
    chatActionRecordingVideo = "recording video"  # noqa: N815
    chatActionUploadingVideo = "uploading video"  # noqa: N815
    chatActionRecordingVoiceNote = "recording voice"  # noqa: N815
    chatActionUploadingVoiceNote = "uploading voice"  # noqa: N815
    chatActionUploadingPhoto = "uploading photo"  # noqa: N815
    chatActionUploadingDocument = "uploading document"  # noqa: N815
    chatActionChoosingLocation = "choosing location"  # noqa: N815
    chatActionChoosingContact = "choosing contact"  # noqa: N815
    chatActionStartPlayingGame = "start playing game"  # noqa: N815
    chatActionRecordingVideoNote = "recording video"  # noqa: N815
    chatActionUploadingVideoNote = "uploading video"  # noqa: N815


class ChatType(Enum):
    chatTypePrivate = "private"  # noqa: N815
    chatTypeBasicGroup = "group"  # noqa: N815
    chatTypeSupergroup = "supergroup"  # noqa: N815
    channel = "channel"
    chatTypeSecret = "secret"  # noqa: N815


class UserStatus(Enum):
    userStatusEmpty = ""  # noqa: N815
    userStatusOnline = "online"  # noqa: N815
    userStatusOffline = "offline"  # noqa: N815
    userStatusRecently = "recently"  # noqa: N815
    userStatusLastWeek = "last week"  # noqa: N815
    userStatusLastMonth = "last month"  # noqa: N815


class UserType(Enum):
    userTypeRegular = ""  # noqa: N815
    userTypeDeleted = "deleted"  # noqa: N815
    userTypeBot = "bot"  # noqa: N815
    userTypeUnknown = "unknownn"  # noqa: N815


class TextParseModeInput(Enum):
    textParseModeMarkdown = "markdown"  # noqa: N815
    textParseModeHTML = "html"  # noqa: N815


class SecretChatState(Enum):
    secretChatStatePending = "pending"  # noqa: N815
    secretChatStateReady = "ready"  # noqa: N815
    secretChatStateClosed = "closed"  # noqa: N815


class Tdlib(Telegram):
    def parse_text_entities(
        self,
        text: str,
        parse_mode: TextParseModeInput = TextParseModeInput.textParseModeMarkdown,
        version: int = 2,
    ) -> AsyncResult:
        """Offline synchronous method which returns parsed entities"""
        data = {
            "@type": "parseTextEntities",
            "text": text,
            "parse_mode": {"@type": parse_mode.name, "version": version},
        }

        return self._send_data(data)

    def send_message(self, chat_id: int, msg: str) -> AsyncResult:
        text = {"@type": "formattedText", "text": msg}

        result = self.parse_text_entities(msg)
        result.wait()
        if not result.error:
            text = result.update

        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageText",
                "text": text,
            },
        }

        return self._send_data(data)

    def download_file(
        self,
        file_id: int,
        priority: int = 16,
        offset: int = 0,
        limit: int = 0,
        synchronous: bool = False,
    ) -> None:
        data = {
            "@type": "downloadFile",
            "file_id": file_id,
            "priority": priority,
            "offset": offset,
            "limit": limit,
            "synchronous": synchronous,
        }
        return self._send_data(data)

    def reply_message(self, chat_id: int, reply_to_message_id: int, text: str) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "reply_to_message_id": reply_to_message_id,
            "input_message_content": {
                "@type": "inputMessageText",
                "text": {"@type": "formattedText", "text": text},
            },
        }

        return self._send_data(data)

    def search_contacts(self, target: str, limit: int = 10) -> AsyncResult:
        data = {"@type": "searchChats", "query": target, "limit": limit}
        return self._send_data(data, block=True)

    def send_doc(self, file_path: str, chat_id: int) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageDocument",
                "document": {"@type": "inputFileLocal", "path": file_path},
            },
        }
        return self._send_data(data)

    def send_audio(self, file_path: str, chat_id: int) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageAudio",
                "audio": {"@type": "inputFileLocal", "path": file_path},
            },
        }
        return self._send_data(data)

    def send_animation(self, file_path: str, chat_id: int) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageAnimation",
                "animation": {"@type": "inputFileLocal", "path": file_path},
            },
        }
        return self._send_data(data)

    def send_photo(self, file_path: str, chat_id: int) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessagePhoto",
                "photo": {"@type": "inputFileLocal", "path": file_path},
            },
        }
        return self._send_data(data)

    def send_video(
        self,
        file_path: Union[str, Path],
        chat_id: int,
        width: int,
        height: int,
        duration: int,
    ) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageVideo",
                "width": width,
                "height": height,
                "duration": duration,
                "video": {"@type": "inputFileLocal", "path": str(file_path)},
            },
        }
        return self._send_data(data)

    def send_voice(
        self, file_path: Union[str, Path], chat_id: int, duration: int, waveform: str
    ) -> AsyncResult:
        data = {
            "@type": "sendMessage",
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageVoiceNote",
                "duration": duration,
                "waveform": waveform,
                "voice_note": {"@type": "inputFileLocal", "path": str(file_path)},
            },
        }
        return self._send_data(data)

    def edit_message_text(self, chat_id: int, message_id: int, text: str) -> AsyncResult:
        data = {
            "@type": "editMessageText",
            "message_id": message_id,
            "chat_id": chat_id,
            "input_message_content": {
                "@type": "inputMessageText",
                "text": {"@type": "formattedText", "text": text},
            },
        }
        return self._send_data(data)

    def toggle_chat_is_marked_as_unread(
        self, chat_id: int, is_marked_as_unread: bool
    ) -> AsyncResult:
        data = {
            "@type": "toggleChatIsMarkedAsUnread",
            "chat_id": chat_id,
            "is_marked_as_unread": is_marked_as_unread,
        }
        return self._send_data(data)

    def toggle_chat_is_pinned(self, chat_id: int, is_pinned: bool) -> AsyncResult:
        data = {
            "@type": "toggleChatIsPinned",
            "chat_id": chat_id,
            "is_pinned": is_pinned,
        }
        return self._send_data(data)

    def set_chat_nottification_settings(
        self, chat_id: int, notification_settings: dict
    ) -> AsyncResult:
        data = {
            "@type": "setChatNotificationSettings",
            "chat_id": chat_id,
            "notification_settings": notification_settings,
        }
        return self._send_data(data)

    def view_messages(
        self, chat_id: int, message_ids: list, force_read: bool = True
    ) -> AsyncResult:
        data = {
            "@type": "viewMessages",
            "chat_id": chat_id,
            "message_ids": message_ids,
            "force_read": force_read,
        }
        return self._send_data(data)

    def open_message_content(self, chat_id: int, message_id: int) -> AsyncResult:
        data = {
            "@type": "openMessageContent",
            "chat_id": chat_id,
            "message_id": message_id,
        }
        return self._send_data(data)

    def forward_messages(
        self,
        chat_id: int,
        from_chat_id: int,
        message_ids: List[int],
        as_album: bool = False,
        send_copy: bool = False,
        remove_caption: bool = False,
        options: Optional[Dict[str, Any]] = None,
    ) -> AsyncResult:
        if options is None:
            options = {}
        data = {
            "@type": "forwardMessages",
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_ids": message_ids,
            "as_album": as_album,
            "send_copy": send_copy,
            "remove_caption": remove_caption,
            "options": options,
        }
        return self._send_data(data)

    def get_basic_group(
        self,
        basic_group_id: int,
    ) -> AsyncResult:
        data = {
            "@type": "getBasicGroup",
            "basic_group_id": basic_group_id,
        }
        return self._send_data(data)

    def get_basic_group_full_info(
        self,
        basic_group_id: int,
    ) -> AsyncResult:
        data = {
            "@type": "getBasicGroupFullInfo",
            "basic_group_id": basic_group_id,
        }
        return self._send_data(data)

    def get_supergroup(
        self,
        supergroup_id: int,
    ) -> AsyncResult:
        data = {
            "@type": "getSupergroup",
            "supergroup_id": supergroup_id,
        }
        return self._send_data(data)

    def get_supergroup_full_info(
        self,
        supergroup_id: int,
    ) -> AsyncResult:
        data = {
            "@type": "getSupergroupFullInfo",
            "supergroup_id": supergroup_id,
        }
        return self._send_data(data)

    def get_secret_chat(
        self,
        secret_chat_id: int,
    ) -> AsyncResult:
        data = {
            "@type": "getSecretChat",
            "secret_chat_id": secret_chat_id,
        }
        return self._send_data(data)

    def send_chat_action(
        self, chat_id: int, action: ChatAction, progress: Optional[int] = None
    ) -> AsyncResult:
        data = {
            "@type": "sendChatAction",
            "chat_id": chat_id,
            "action": {"@type": action.name, "progress": progress},
        }
        return self._send_data(data)

    def get_contacts(self) -> AsyncResult:
        data = {
            "@type": "getContacts",
        }
        return self._send_data(data)

    def leave_chat(self, chat_id: int) -> AsyncResult:
        data = {
            "@type": "leaveChat",
            "chat_id": chat_id,
        }
        return self._send_data(data)

    def join_chat(self, chat_id: int) -> AsyncResult:
        data = {
            "@type": "joinChat",
            "chat_id": chat_id,
        }
        return self._send_data(data)

    def close_secret_chat(self, secret_chat_id: int) -> AsyncResult:
        data = {
            "@type": "closeSecretChat",
            "secret_chat_id": secret_chat_id,
        }
        return self._send_data(data)

    def create_new_secret_chat(self, user_id: int) -> AsyncResult:
        data = {
            "@type": "createNewSecretChat",
            "user_id": user_id,
        }
        return self._send_data(data)

    def create_new_basic_group_chat(self, user_ids: List[int], title: str) -> AsyncResult:
        data = {
            "@type": "createNewBasicGroupChat",
            "user_ids": user_ids,
            "title": title,
        }
        return self._send_data(data)

    def delete_chat_history(
        self, chat_id: int, remove_from_chat_list: bool, revoke: bool = False
    ) -> AsyncResult:
        """
        revoke: Pass true to try to delete chat history for all users
        """
        data = {
            "@type": "deleteChatHistory",
            "chat_id": chat_id,
            "remove_from_chat_list": remove_from_chat_list,
            "revoke": revoke,
        }
        return self._send_data(data)

    def get_user(self, user_id: int) -> AsyncResult:
        data = {
            "@type": "getUser",
            "user_id": user_id,
        }
        return self._send_data(data)

    def get_user_full_info(self, user_id: int) -> AsyncResult:
        data = {
            "@type": "getUserFullInfo",
            "user_id": user_id,
        }
        return self._send_data(data)


def get_chat_type(chat: Dict[str, Any]) -> Optional[ChatType]:
    try:
        chat_type = ChatType[chat["type"]["@type"]]
        if chat_type == ChatType.chatTypeSupergroup and chat["type"]["is_channel"]:
            chat_type = ChatType.channel
        return chat_type
    except KeyError:
        pass
    return None


def is_group(chat_type: Union[str, ChatType]) -> bool:
    return chat_type in (
        ChatType.chatTypeSupergroup,
        ChatType.chatTypeBasicGroup,
    )
