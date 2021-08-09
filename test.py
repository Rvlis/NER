import spacy
import os
import argparse


def pos_of_token(input_text):
    """
    打印词性标签
    """
    nlp = spacy.load("en_core_web_md")
    doc = nlp(input_text)
    for token in doc:
        print("Token: {}, POS:{}, TAG:{}".format(token.text, token.pos_, token.tag_))

def LR_based_NER(input_text):
    """
    使用预训练语言模型的命名实体识别
    param: input_text
    return: None
    """
    # 1. 加载预训练模型，生成nlp对象（即处理文本的管道pipeline）
    # 加载的模型名称以自己下载的为准
    nlp = spacy.load("en_core_web_md")
    # 2. nlp对象解析文本，得到doc对象，此时doc对象已经包含了文本的诸多数据，包括识别的实体
    doc = nlp(input_text)
    
    # 3. 遍历doc.ents，它存放了识别的实体及其信息
    for ent in doc.ents:
        # 打印实体名称、类型和位置
        print("Entity: {}, Label: {}".format(ent.text, ent.label_), (ent.start, ent.end))

def rule_based_NER(input_text):
    """
    基于规则的命名实体识别
    """
    # 同上
    nlp = spacy.load("en_core_web_md")
    # 1. 添加组件entity_ruler, 它允许我们通过自定义规则来抽取特定实体
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})

    # 2. 定义匹配模板
    # 一般而言，patterns格式：[{"label": , "pattern": }, ...]
    patterns = [
        # 针对前后类型不一致，使用精确字符串匹配并指定标签
        {"label":"ORG", "pattern":"Nanhang"},

        # 针对没有识别出特定实体，使用基于词性的正则匹配
        # 区分pos标签和tag标签的异同：https://spacy.io/api/annotation
        {"label":"TITLE", "pattern":[{"POS":"PROPN"}, {"POS":"PROPN"}, {"POS":"PROPN"}, {"POS":"PROPN"}, {"POS":"PROPN"}]},
        # {"label":"TITLE", "pattern":[{"POS":"PROPN"}, {"POS":"PROPN"}, {"POS":"PROPN"}, {"POS":"PROPN", "OP":"+"}]},
        # {"label":"TITLE", "pattern":[{"TAG":"NNP"}, {"TAG":"NNP"}, {"TAG":"NNP"}, {"TAG":"NNP"}, {"TAG":"NNP"}]}
    ] 
    # 3. 添加模板
    ruler.add_patterns(patterns)
    # 4. 同上
    doc = nlp(input_text)
    for ent in doc.ents:
        print("Entity: {}, Label: {}".format(ent.text, ent.label_), (ent.start, ent.end))
    

if __name__ == "__main__":
    
    text = """
        Nanjing University of Aeronautics and Astronautics (NUAA), known colloquially as Nanhang, is an elite Double First Class Discipline University. 
        Located in Nanjing, Jiangsu province, it was established in 1952 and is now operated by the Chinese Ministry of Industry and Information Technology. 
        Nanhang has three campuses: the Ming Palace Campus situated on the ruins of a Ming Palace, and the Jiangjun Road Campus situated in the Jiangning Economic and Technological Development Zone. 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", type=str, choices=["lr", "rule"], help="choose method of NER")
    parser.add_argument("-p", "--pos", type=str, default="", help="pos of token")
    args = parser.parse_args()
    
    if args.method == "lr":
        LR_based_NER(text)
    elif args.method == "rule":
        rule_based_NER(text)
    
    if args.pos != "":
        pos_of_token(args.pos)
    