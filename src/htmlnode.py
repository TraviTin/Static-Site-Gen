


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


