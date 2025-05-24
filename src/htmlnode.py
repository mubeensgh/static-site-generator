class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        #tag and value are strings, children are HTMLNode Objects
        #props are a dictionary of key value pairs representing atribute and values
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        #children will override this
        pass
    def props_to_html(self):
        res = ""
        if self.props == None:
            return res
        for i,j in self.props.items():
            res+= f' {i}="{j}"'
        return res
    def __repr__(self):
        return f'tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("LeafNode requires a value.")
        super().__init__(tag, value, children=[], props=props)
    def to_html(self):
        if self.tag == None:
            return str(self.value)
        return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        #tag and children are mandatory!! - therefore, no value argument
        if tag is None:
            raise ValueError("ParentNode requires a tag.")
        if not children:
            raise ValueError("ParentNode requires at least one child.")

        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag to render HTML.")
        if not self.children:
            raise ValueError("ParentNode must have children to render HTML.")

        # init the children html
        children_html = ""        
        #loop first for each item in children
        for child in self.children:
            #children_html = child.to_html()
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'