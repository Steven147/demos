import json
from datetime import datetime

from application import app, db
from model.db_model.map.mapping import Mapping
from model.db_model.document import Document
from model.db_model.map.class_info import ClassInfo
from model.db_model.map.option import Option


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Document': Document, 'ClassInfo': ClassInfo, 'Option': Option}


# map - options
# option - class_info
class DBModel:
    def __init__(self):
        # 创建表的语句
        with app.app_context():
            db.create_all()
            self.session = db.session
            # self._init_data()

    def reset_class_db(self):
        self._init_data()

    def _init_data(self):
        for m in [Mapping, Option, ClassInfo]:
            self.clear_database(m)
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
                    '通用关系类': '05',
                    # '生命成长类': 'I',
                    # '亲子关系类': 'II',
                    # '孝亲关系类': 'III',
                    # '夫妻关系类': 'IV',
                    # '通用关系类': 'V',
                }
            },
            'class_name': {
                'text': "请输入课程名称",
                'placeholder': "课程名称",
                'option': {
                    '网络七期': 'VwrUwqamZiGRpGkndmGcFBJhn2d',
                    '未来八期': 'LU46wq2kIixvGVkfenqcX4bMnfc',
                }
            }
        }

        class_info = {
            'LU46wq2kIixvGVkfenqcX4bMnfc': {
                'name': '未来八期',
                'fullname': '“我们是中国的未来”孝亲反哺专场第8期',
                'time': '20231015'
            },
            'VwrUwqamZiGRpGkndmGcFBJhn2d': {
                'name': '网络七期',
                'fullname': '网络基础班第七期',
                'time': '20221019'
            },
        }
        for key, details in mappings.items():
            # 创建 Mapping
            mapping_instance = Mapping(
                field_name=key,
                text=details['text'],
                placeholder=details['placeholder'],
            )
            db.session.add(mapping_instance)
            # 创建 Option
            for option_text, option_value in details['option'].items():
                # 检查是否是 ClassInfo 的 key
                class_info_instance = None
                if option_value in class_info:
                    class_info_detail = class_info[option_value]
                    # 创建 ClassInfo 是必要的
                    class_info_instance = ClassInfo(
                        id=option_value,
                        name=class_info_detail['name'],
                        fullname=class_info_detail['fullname'],
                        time=class_info_detail['time'],
                    )
                    db.session.add(class_info_instance)

                option_instance = Option(
                    name=option_text,
                    value=option_value,
                    mapping=mapping_instance,
                    class_info=class_info_instance
                )
                db.session.add(option_instance)

        # 提交所有更改
        db.session.commit()

    def add_option(self, field_name: str, option_name: str, option_value: str, class_info_data: dict = None):
        mapping_instance = db.session.query(Mapping).filter_by(field_name=field_name).first()

        if not mapping_instance:
            raise ValueError("No mapping found with field_name: ", field_name)

        class_info_instance = None
        if class_info_data:
            class_info_instance = ClassInfo(
                id=class_info_data.get('id'),
                name=class_info_data.get('name'),
                fullname=class_info_data.get('full_name'),
                time=class_info_data.get('time'),
            )
            db.session.add(class_info_instance)

        option_instance = Option(
            name=option_name,
            value=option_value,
            mapping=mapping_instance,
            class_info=class_info_instance
        )

        db.session.add(option_instance)
        db.session.commit()

    def get_class_name_time(self, id: str, time: str = None):
        class_info = self.session.query(ClassInfo).get(id)
        if class_info:
            if not time:
                time = class_info.time
            return f"{class_info.name}{time}"
        return None

    def get_class_fullname(self, id: str):
        class_info = self.session.query(ClassInfo).get(id)
        if class_info:
            return class_info.fullname
        return None

    def get_timestamp_version(self, version: str = '一'):
        # 获取当前时间
        now = datetime.now()
        # 格式化日期
        formatted_date = now.strftime("%Y%m%d")
        return f"{formatted_date}第{version}版"

    def map_option(self, field_name: str, option_name: str):
        option = self.session.query(Option).join(Mapping).filter(
            Mapping.field_name == field_name, Option.name == option_name
        ).first()
        if option:
            return option.value
        return None

    def get_option_suggest(self, field_name: str):
        mapping = self.session.query(Mapping).filter_by(field_name=field_name).first()
        if mapping:
            options = [opt.name for opt in mapping.options]
            return f"{mapping.text}({'、'.join(options)}):"
        return None

    def get_option_value(self, field_name: str):
        mapping = self.session.query(Mapping).filter_by(field_name=field_name).first()
        if mapping:
            options = [opt.value for opt in mapping.options]
            return f"{mapping.text}({'、'.join(options)}):"

    def get_mapping_records(self):
        return self.session.query(Mapping).all()

    # code_title: B04001孩子对父母的日常表达
    # code: B04001
    # code_stamp: D04001未来八期20231015

    # def set_manual_record(mapped_category, mapped_section, mapped_relationship, mapped_parent_token, document_number, title):
    #     """
    #     set record manually, count new document bigger than others in the same type
    #     """
    #
    #     return set_new_doc(
    #         mapped_category,
    #         mapped_section,
    #         mapped_relationship,
    #         document_number,
    #         title,
    #         token='',
    #         obj_token='',
    #         mapped_parent_token=mapped_parent_token,
    #     )

    def find_manual_record(self, mapped_category, mapped_section, mapped_relationship, document_number_str):
        """
        set record manually, count new document bigger than others in the same type
        """
        return self.session.query(Document).filter_by(
            category=mapped_category, section=mapped_section, relationship=mapped_relationship,
            document_number=int(document_number_str)
        ).order_by(
            Document.document_number.desc()
        ).first()

    def find_all_records(self, class_name: str):
        return self.session.query(Document).filter_by(
            parent_token=self.map_option('class_name', class_name)
        ).order_by(
            Document.document_number
        ).all()

    # def find_class_record(message: str):

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
    #             db.session.delete(result)
    #
    #     set_new_doc(mapped_category, mapped_section, mapped_relationship, document_number, title)

    # def set_new_doc(mapped_category, mapped_section, mapped_relationship, document_number,
    #                 title, token, obj_token, mapped_parent_token):
    #     new_doc = Document(
    #         category=mapped_category,
    #         section=mapped_section,
    #         relationship=mapped_relationship,
    #         document_number=int(document_number),
    #         title=title,
    #         token=token,
    #         obj_token=obj_token,
    #         parent_token=mapped_parent_token
    #     )
    #     new_doc.print_doc()
    #     db.session.add(new_doc)
    #     db.session.commit()
    #     return new_doc

    def get_code_title_list(self, code_title: str):
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

    def map_manual_input(self, message: str):
        category, section, relationship, class_name, title = message.split("、")
        # 获取用户输入
        # category = input(Mappings.get_option_suggest('category'))
        # section = input(Mappings.get_option_suggest('section'))
        # relationship = input(Mappings.get_option_suggest('relationship'))
        # title = input('请输入标题:')

        # 映射输入
        mapped_category = self.map_option("category", category)
        mapped_section = self.map_option("section", section)
        mapped_relationship = self.map_option("relationship", relationship)
        mapped_parent_token = self.map_option("class_name", class_name)
        return mapped_category, mapped_section, mapped_relationship, mapped_parent_token, title

    def get_next_document_number(self, mapped_category, mapped_section, mapped_relationship):
        result = self.get_results(mapped_category, mapped_section, mapped_relationship)
        if result and result.first():
            document_number = result.first().document_number + 1
        else:
            document_number = 1
        return document_number

    def get_results(self, mapped_category, mapped_section, mapped_relationship):
        # 获取数据库中同一分类、版块和关系下最大的文档编号
        return self.session.query(Document).filter_by(
            category=mapped_category, section=mapped_section, relationship=mapped_relationship
        ).order_by(
            Document.document_number.desc()
        )

    def show_record(self):
        # 查询
        docs = self.session.query(Document).filter(Document.id > 0)
        # 显示查询结果
        for doc in docs:
            doc.get_code_title()

    def new_doc(self,
                document_number,
                category,
                parent_token,
                relationship,
                section,
                title,
                token='',
                obj_token=''
                ):
        new_doc = Document(  # without token and obj token before callback
            category=category,
            section=section,
            relationship=relationship,
            document_number=document_number,
            parent_token=parent_token,
            title=title,
            token=token,
            obj_token=obj_token
        )
        return new_doc

    def new_class(
            self, ):
        pass

    def clear_document(self):
        self.clear_database(Document)

    def clear_database(self, model: db.Model):
        self.session.query(model).delete(synchronize_session=False)
        self.session.commit()

    def get_doc_sub_title(self, new_doc: Document):
        return f"{new_doc.get_codes()}{self.get_class_name_time(new_doc.parent_token)}"

    # @staticmethod
    # def get_code(category, section, relationship, document_number):
    #     print(f"[print_code] code: {category} {section} " +
    #           f"{relationship} {document_number:03d}")
    #     return f"{category}{section}{relationship}{document_number:03d}"

    def commit_add_doc(self, new_doc: Document):
        new_doc.print_doc()
        self.session.add(new_doc)
        self.session.commit()
