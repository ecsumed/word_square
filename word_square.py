import treelib
from treelib import Tree

WORDS_FILE = 'words.txt'

tree = Tree()
word = ''
word_len = None
square_found = None


def word_match(f_name, match_str, word_length):
    """
        Reads words from the specified file. Matches the beginning of the string
        and the word length.

        INPUT:
            match_str = 'do'
            length = 3

        OUTPUT:
            ['dog', 'don', 'dom', ...]
    """
    words = []
    with open(f_name, 'r') as f:
        for line_no, line in enumerate(f):
            line = line.strip()
            if line\
                    and line.startswith(match_str)\
                    and len(line) == word_length:
                words.append(line)
    return words


def make_tree(letter, first, index):
    global square_found
    global word_len
    global word

    words = word_match(WORDS_FILE, letter, word_len)

    for w in words:
        if first:
            tree.create_node(w, w, parent=word)
            if tree.depth(w) == word_len - 1:
                square_found = w
                break
        else:
            nodes = [tree[node].tag
                     for node in tree.expand_tree(mode=Tree.DEPTH)]

            for node in nodes:
                if tree.depth(node) == index:
                    path = get_path(node)
                    match_str = make_regex(path, index)

                    # sub_tree = word_match(WORDS_FILE, match_str, word_len)
                    sub_tree = [word for word in words
                                if word.startswith(match_str)]

                    if sub_tree:
                        for child_node in sub_tree:
                            try:
                                tree.create_node(child_node,
                                                 child_node,
                                                 parent=node)

                                if tree.depth(child_node) == word_len - 1:
                                    square_found = child_node
                                    break
                            except treelib.tree.DuplicatedNodeIdError:
                                continue
                if square_found:
                    break
    return


def make_regex(path, index):
    """
        Creates a regex from the tree path, so that the child  nodes can contain
        that pattern.
        Example tree:
            dog
            I-- out
            I-- one
            I-- orc

        INPUT:
            path = ['dog', 'out']
            index = 2

        OUTPUT:
            'gt'

    """
    # Index of the next letter in the word being processed.
    # Increment because root was not counted
    index += 1

    if len(path) > index:
        path = path[:-1]

    regex = ''
    for node in path:
        regex += node[index]
    return regex


def get_path(node):
    """
        Returns the path to the specified node.
        Example Tree:
            root
            I-- a1
            I-- b1
                I-- b2
        INPUT:
            treelib.Node object: b2

        OUTPUT:
            a path list, for ex.: ['root', 'b1', 'b2']
    """
    paths = tree.paths_to_leaves()
    for path in paths:
        if node in path:
            return path


def pretty_str(word_square):
    """
        Returns a visually pleasing string of the square.
    """
    print_str = ''
    for word in word_square:
        print_str += ' '.join(list(word)) + '\n'

    return print_str


def word_square(word):
    """
        Given a word, will attempt to create a square.

        INPUT:
            'dog'

        OUTPUT:
            d o g
            o a r
            g r a
    """
    tree.create_node(word, word)  # root node

    first = True
    for index, letter in enumerate(list(word[1:])):
        make_tree(letter, first, index)

        if square_found:
            break

        first = False

    if square_found:
        return pretty_str(get_path(square_found))
    else:
        return 'No square found'


def main():
    global square_found
    global word_len
    global word

    word = raw_input("Enter the word: ")
    word_len = len(word)

    print word_square(word)


if __name__ == '__main__':
    main()
