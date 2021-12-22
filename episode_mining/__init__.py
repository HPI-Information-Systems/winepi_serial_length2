# coding: utf-8

class WINEPIRule(object):
    def __init__(self, antecedent, consequent, width, supp, conf):
        self.antecedent = antecedent
        self.consequent = consequent
        self.width = width
        self.supp = supp
        self.conf = conf

    def __repr__(self):
        return '{}: {} ==> {} [{}] [{}, {}]'.format(
            type(self).__name__, self.antecedent,
            self.consequent, self.width, self.supp, self.conf
        )