from .basicai import BasicAI

ai_class_dict = {"BasicAI": BasicAI}


def get_ai_class(string):
    return ai_class_dict[string]
