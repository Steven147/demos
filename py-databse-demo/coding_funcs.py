from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)
    section = Column(String)
    relationship = Column(String)
    document_number = Column(Integer)


# 创建engine，并连接SQLite数据库
engine = create_engine('sqlite:///test.db')

# 创建Session对象
Session = sessionmaker(bind=engine)

# 创建表的语句
Base.metadata.create_all(engine)

session = Session()

# 定义映射规则
mappings = {
    '秘笈A': 'A',
    '表达B': 'B',
    '行为C': 'C',
    '操作D': 'D',
    '爱相伴01': '01',
    '爱相随02': '02',
    '爱相遇03': '03',
    '爱未来04': '04',
    '01生命成长类': '01',
    '11亲子关系类': '11',
    '12孝亲关系类': '12',
    '13夫妻关系类': '13'
}


def set_record():
    # 获取用户输入
    # category = input('请输入文档分类（秘笈A、表达B、行为C、操作D）：')
    # section = input('请输入版块（爱相伴01、爱相随02、爱相遇03、爱未来04）：')
    # relationship = input('请输入关系（01生命成长类、11亲子关系类、12孝亲关系类、13夫妻关系类）：')
    category = '秘笈A'
    section = '爱未来04'
    relationship = '12孝亲关系类'

    # 映射输入
    mapped_category = mappings.get(category, '')
    mapped_section = mappings.get(section, '')
    mapped_relationship = mappings.get(relationship, '')

    # 获取数据库中同一分类、版块和关系下最大的文档编号
    result = session.query(Document).filter_by(
        category=mapped_category, section=mapped_section, relationship=mapped_relationship
    ).order_by(
        Document.document_number.desc()
    ).first()

    if result:
        document_number = result.document_number + 1
    else:
        document_number = 1

    new_doc = Document(category=mapped_category, section=mapped_section, relationship=mapped_relationship,
                       document_number=document_number)
    session.add(new_doc)
    session.commit()



def get_record():
    # 查询年龄大于25的员工
    docs = session.query(Document).filter(Document.id > 0)
    # 显示查询结果
    for doc in docs:
        print(doc.category, doc.section, doc.relationship, doc.document_number)


if __name__ == "__main__":
    set_record()
    get_record()
