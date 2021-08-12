class ClassLabel(object):
    def __call__(self, target):
        return target['label']
