


class HtmlNode:
    def __init__(
            self,
            tag: str | None = None,
            value: str | None = None ,
            children: list["HtmlNode"] | None = None,
            props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        html_props = ""
        for entries in self.props:
            html_props += f' {entries}="{self.props[entries]}"'
        return html_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HtmlNode):
    def __init__(
    self,
    tag: str | None,
    value: str,
    props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HtmlNode):
    def __init__(
            self,
            tag: str,
            children: list["HtmlNode"],
            props: dict[str, str] | None = None,
    )-> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid Node: no children, not a ParentNode")
        child_strings = ""
        for child in self.children:
            child_strings += child.to_html()
        html_full_parent_string = f"<{self.tag}{self.props_to_html()}>{child_strings}</{self.tag}>"
        return html_full_parent_string

