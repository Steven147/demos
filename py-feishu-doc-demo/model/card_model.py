import json
from typing import List

from model.db_model.map.mapping import Mapping


class CardModel:
    # todo use online card, save url or key in model instance
    @staticmethod
    def _get_options(map: Mapping, tag: str = "plain_text"):
        return [
            {
                "text": {
                    "tag": tag,
                    "content": option.name
                },
                "value": option.value
            }
            for option in map.options
        ]

    @staticmethod
    def _get_options_element(map: Mapping):
        options = CardModel._get_options(map)
        return {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": map.text
            },
            "extra": {
                "tag": "select_static",
                "placeholder": {
                    "tag": "plain_text",
                    "content": map.placeholder
                },
                "value": {
                    "key": map.field_name
                },
                "options": options
            }
        }
    @staticmethod
    def _get_button_element(text: str):
        return {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": text
            },
            "extra": {
                "tag": "button",
                "text": {
                    "tag": "lark_md",
                    "content": "确认"
                },
                "type": "primary",
                "value": {
                    "key": "confirm"
                }
            }
        }

    def generate_elements(self, maps: List[Mapping]):
        elements = []
        for map in maps:
            elements.append(
                CardModel._get_options_element(map)
            )
        elements.append(
            CardModel._get_button_element(
                text="选择完成后，点击确认，会自动生成文档对应的**编码**。"
                     "\n同时会以编码作为标题在知识库中新建文档，返回文档**链接**。",

            )
        )
        return elements
    #
    # def generate_class_elements(self, maps: List[Mapping]):
    #

    def get_card_source_string(self, maps: List[Mapping]):
        # data = {}
        # if len(key) <= 0:
        #     pass
        # elif "生成" in key:
        data = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": "文档编码生成卡片"
                }
            },
            "card_link": {
                "url": "",
                "pc_url": "",
                "android_url": "",
                "ios_url": ""
            },
            "elements": self.generate_elements(maps),
        }


        # print('[get_card_source_string]:' + json.dumps(data, indent=2, ensure_ascii=False))
        return json.dumps(data, separators=(',', ':'))

