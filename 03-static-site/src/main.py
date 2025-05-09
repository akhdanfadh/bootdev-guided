from .textnode import TextNode, TextType


def main():
    text_node_1 = TextNode("Hello, world!", TextType.TEXT)
    text_node_2 = TextNode("This is a test.", TextType.LINK, "https://www.google.com")

    print(text_node_1)
    print(text_node_2)
    print(text_node_1 == text_node_2)


if __name__ == "__main__":
    main()
