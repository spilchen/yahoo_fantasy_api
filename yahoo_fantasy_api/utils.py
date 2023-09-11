from xml.dom.minidom import Document, Element


def create_element(doc: Document, parent: Element, name: str, text: str) -> None:
    element = doc.createElement(name)
    element.appendChild(doc.createTextNode(text))
    parent.appendChild(element)
