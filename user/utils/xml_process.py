def element_to_dict(element):
    """
    递归函数将Element转换为dict
    """
    dict_ = {}
    # 获取Element的所有属性
    dict_.update(element.attrib)
    # 遍历所有子元素
    for child in element:
        # 如果子元素是一个Element，将其转换为dict并添加到当前字典中
        if child:
            dict_[child.tag] = element_to_dict(child)
        # 否则，将子元素的值添加到当前字典中
        else:
            dict_[child.tag] = child.text
    return dict_
