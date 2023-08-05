from .tools import DictAsMember
from .rule import Rule

def parse_document_rules(config):
    document_names = parse_documents_name(config)
    default_rules = parse_default_document_rules(config)
    document_rules = {}
    for document_name in document_names:
        document_rules[document_name] = parse_specific_document_rules(config[document_name], default_rules)
    return document_rules


def parse_documents_name(config):
    document_names = []
    for key, value in config.items():
        if not key in Rule.reserved:
            document_names.append(key)
    return document_names


def parse_default_document_rules(config):
    default_rule = Rule(config)
    return default_rule


def parse_specific_document_rules(config, default_rules):
    specific = default_rules.copy()
    specific.set_config(config)
    return specific
