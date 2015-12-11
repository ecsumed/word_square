import treelib
from treelib import Tree

WORDS_FILE = 'words'

tree = Tree()
squares = []
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
                if tree.depth(node) == (index):
                    path = get_path(node)
                    match_str = make_regex(path, index)

                    sub_tree = word_match(WORDS_FILE, match_str, word_len)

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
        Ex.
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


def pretty_print(word_square):
    """
        Pretty prints the word square.
    """
    for word in word_square:
        print ' '.join(list(word))


def main():
    global square_found
    global word_len
    global word

    word = raw_input("Enter the word: ")
    word_len = len(word)

    tree.create_node(word, word)  # root node

    first = True
    for index, letter in enumerate(list(word[1:])):
        make_tree(letter, first, index)
        # print tree.show()

        if square_found:
            break

        first = False

    if square_found:
        pretty_print(get_path(square_found))
    else:
        print 'No square found'

if __name__ == '__main__':
    main()
