from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import json

Base = declarative_base()


# 要定义在 create session 之前
class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)
    section = Column(String)
    relationship = Column(String)
    document_number = Column(Integer)
    title = Column(String(50))
    token = Column(String(30))
    parent_token = Column(String(30))

    def get_code_title(self):
        print(f"[show_record] code_title: {self.category} {self.section} " +
              f"{self.relationship} {self.document_number:03d} {self.title}")
        return f"{self.category}{self.section}{self.relationship}{self.document_number:03d}{self.title}"

    @staticmethod
    def get_code(category, section, relationship, document_number):
        print(f"[print_code] code: {category} {section} " +
              f"{relationship} {document_number:03d}")
        return f"{category}{section}{relationship}{document_number:03d}"

    @staticmethod
    def commit_session():
        session.commit()


# 创建engine，并连接SQLite数据库
engine = create_engine('sqlite:///test.db')

# 创建Session对象
Session = sessionmaker(bind=engine)

# 创建表的语句
Base.metadata.create_all(engine)

session = Session()


class Mappings:
    # 定义映射规则
    mappings = {
        'category': {
            'text': "请输入文档分类",
            'placeholder': "文档分类",
            'option': {
                '秘笈': 'A',
                '表达': 'B',
                '行为': 'C',
                '操作': 'D',
            }
        },
        'section': {
            'text': "请输入版块",
            'placeholder': "版块",
            'option': {
                '爱相伴': '01',
                '爱相随': '02',
                '爱相遇': '03',
                '爱未来': '04',
                '不确定': '05',
            }
        },
        'relationship': {
            'text': "请输入关系",
            'placeholder': "关系",
            'option': {
                '生命成长类': '01',
                '亲子关系类': '02',
                '孝亲关系类': '03',
                '夫妻关系类': '04',
                '通用关系类': '00',
                # '生命成长类': 'I',
                # '亲子关系类': 'II',
                # '孝亲关系类': 'III',
                # '夫妻关系类': 'IV',
                # '通用关系类': 'V',
            }
        },
        'class_name': {
            'text': "请输入课程名称",
            'option': {
                '网络七期': 'VwrUwqamZiGRpGkndmGcFBJhn2d',
                '亲子关系类': 'LU46wq2kIixvGVkfenqcX4bMnfc',
            }
        }
    }

    @staticmethod
    def get_option_suggest(key: str):
        value = Mappings.mappings.get(key)
        return f"{value.get('text')}({'、'.join(value.get('option').keys())}):"

    @staticmethod
    def map_option(key: str, option_str: str):
        return Mappings.mappings.get(key).get('option').get(option_str)


def generate_elements(result: str):
    elements = []
    for key, details in Mappings.mappings.items():
        options = [
            {
                "text": {
                    "tag": "plain_text",
                    "content": text
                },
                "value": value
            }
            for text, value in details['option'].items()
        ]
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": details['text']
            },
            "extra": {
                "tag": "select_static",
                "placeholder": {
                    "tag": "plain_text",
                    "content": details['placeholder']
                },
                "value": {
                    "key": key
                },
                "options": options
            }
        })
    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "选择完成后，点击确认，会自动生成文档对应的**编码**。" + result +
                           "\n同时会以编码作为标题在知识库中新建文档，返回文档**链接**。"
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
    )
    return elements


def get_card_source_string(result=''):
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
        "elements": generate_elements(result),
    }
    # print('[get_card_source_string]:' + json.dumps(data, indent=2, ensure_ascii=False))
    return json.dumps(data, separators=(',', ':'))


# code_title: B04001孩子对父母的日常表达
# code: B04001
# code_stamp: D04001未来八期20231015

def get_origin_code_titles():
    return [
        "B04III001孩子对父母的日常表达",
        "B04III002孩子犯错后向父母说的四句话",
        "A04III001中国当代青年的样子",
        "A04III002爱反哺的三个对象",
        "A04III003爱与幸福——青年优秀的四个阶段",
        "A04III004千万不要回报父母",
        "A04III005至德要道",
        "D04III001孝父母的第一步",
    ]


def set_manual_record(message: str):
    """
    set record manually, count new document bigger than others in the same type
    """
    params = map_manual_input(message)
    mapped_category, mapped_section, mapped_relationship, mapped_parent_token, title = params
    document_number = get_next_document_number(mapped_category, mapped_section, mapped_relationship)

    return set_new_doc(
        mapped_category,
        mapped_section,
        mapped_relationship,
        document_number,
        title,
        token='',
        mapped_parent_token=mapped_parent_token,
    )


def find_manual_record(message: str):
    """
    set record manually, count new document bigger than others in the same type
    """
    mapped_category, mapped_section, mapped_relationship, document_number_str, _ = (
        get_code_title_list(message))
    return session.query(Document).filter_by(
        category=mapped_category, section=mapped_section, relationship=mapped_relationship,
        document_number=int(document_number_str)
    ).order_by(
        Document.document_number.desc()
    ).first()


# def set_record_with_code_title(code_title: str):
#     """
#     :param code_title:
#     set record with code title, if exited, delete record
#     """
#     mapped_category, mapped_section, mapped_relationship, document_number, title = get_code_title_list(code_title)
#
#     # 去重复
#     for result in get_results(mapped_category, mapped_section, mapped_relationship):
#         if result.document_number == document_number:
#             print("[set_record_with_code_title] document_number duplicated, force replace title")
#             session.delete(result)
#
#     set_new_doc(mapped_category, mapped_section, mapped_relationship, document_number, title)


def set_new_doc(mapped_category, mapped_section, mapped_relationship, document_number, title, token, mapped_parent_token):
    new_doc = Document(
        category=mapped_category,
        section=mapped_section,
        relationship=mapped_relationship,
        document_number=int(document_number),
        title=title,
        token=token,
        parent_token=mapped_parent_token
    )
    new_doc.get_code_title()
    session.add(new_doc)
    session.commit()
    return new_doc


def get_code_title_list(code_title: str):
    code_lengths = [1, 2, 2, 3]
    if len(code_title) < sum(code_lengths):
        return
    result = []
    start = 0
    for length in code_lengths:
        # 切片字符串
        part = code_title[start:start + length]
        result.append(part)
        # 滑动窗口
        start += length

    result.append(code_title[start:])
    print("[get_code_title_list] result", result)
    return result


def map_manual_input(message: str):
    category, section, relationship, class_name, title = message.split("、")
    # 获取用户输入
    # category = input(Mappings.get_option_suggest('category'))
    # section = input(Mappings.get_option_suggest('section'))
    # relationship = input(Mappings.get_option_suggest('relationship'))
    # title = input('请输入标题:')

    # 映射输入
    mapped_category = Mappings.map_option("category", category)
    mapped_section = Mappings.map_option("section", section)
    mapped_relationship = Mappings.map_option("relationship", relationship)
    mapped_parent_token = Mappings.map_option("class_name", class_name)
    return mapped_category, mapped_section, mapped_relationship, mapped_parent_token, title


def get_next_document_number(mapped_category, mapped_section, mapped_relationship):
    result = get_results(mapped_category, mapped_section, mapped_relationship)
    if result and result.first():
        document_number = result.first().document_number + 1
    else:
        document_number = 1
    return document_number


def get_results(mapped_category, mapped_section, mapped_relationship):
    # 获取数据库中同一分类、版块和关系下最大的文档编号
    return session.query(Document).filter_by(
        category=mapped_category, section=mapped_section, relationship=mapped_relationship
    ).order_by(
        Document.document_number.desc()
    )


def show_record():
    # 查询
    docs = session.query(Document).filter(Document.id > 0)
    # 显示查询结果
    for doc in docs:
        doc.get_code_title()


if __name__ == "__main__":
    # print(get_card_source_string())
    # set_manual_record()
    # for code_title in get_origin_code_titles():
    #     set_record_with_code_title(code_title)
    # show_record()
    pass
