# defining constants
ALPHABET_START = 36
ALPHABET_END = 126
ALPHABET_LENGTH = ALPHABET_END - ALPHABET_START + 1

class End:
    """
    Class to represent the end of an edge in the suffix tree.

    Attribute:
        value: An optional value representing the end of an edge in the tree.
    """

    def __init__(self, value=None):
        self.value = value

class Node:
    """
    Class to represent a node in the suffix tree.

    Attributes:
        edges (list): A list of edges for this node, with a length equal to the number of characters in the defined alphabet.
                      Each index in the list corresponds to a character.
        
        link (Node or None): A reference to the suffix link of this node. This link is used to efficiently traverse the tree
                             during the construction process and during searches.
    """

    def __init__(self):
        self.edges = [None] * ALPHABET_LENGTH
        self.link = None

class Edge:
    """
    Class to represent an edge in the suffix tree.

    Each edge connects a parent node to a child node in the tree. An edge is defined by its start and end positions in the string, 
    along with an optional suffix ID that indicates which suffix the edge belongs to.

    Attributes:
        start (int): The starting index of the substring represented by this edge in the original string.

        end (End): An instance of the End class that marks the end of the substring represented by this edge.

        next (Node or None): A reference to the child node that is reached by traversing this edge. It is initialised to 
                             None and set during tree construction.

        suffix_id (int or None): An optional identifier for the suffix associated with this edge. This can be 
                                 used for locating specific suffixes in the string.

    Methods:
        __len__(): Returns the length of the edge, calculated through the difference between the end and start positions, 
                   adjusted for the index representation.
    """

    def __init__(self, start, end, suffix_id=None):
        self.start = start
        self.end = end
        self.next = None
        self.suffix_id = suffix_id

    def __len__(self):
        return self.end.value - self.start + 1

class ActivePoint:
    """
    Class to maintain the active point in the suffix tree during construction.

    The active point consists of:
    - active_node: the current node being processed in the suffix tree.
    - active_edge: the index of the character in the text representing the current edge.
    - active_length: how far along the current active edge we are.

    This class is to efficiently manage the traversal and construction of the suffix tree using Ukkonen's algorithm.

    Attributes:
        active_node (Node): The current node in the suffix tree.
        active_edge (int or None): The index of the active edge in the text.
        active_length (int): The length along the active edge that has been matched.

    Methods:
        update_active_edge(i): Updates the active edge index based on the current position in the text.
    """
    
    def __init__(self, root):
         # start at root
        self.active_node = root
        self.active_edge = None
        self.active_length = 0

    def update_active_edge(self, i):
        # set active edge to the current index if no length is matched
        if self.active_length == 0:
            self.active_edge = i

class Ukkonen:
    """
    This class implements Ukkonen's algorithm for constructing a suffix tree for a given text.

    Attributes:
        text (str): The input text for which the suffix tree is constructed, with a unique terminator ($) appended.
        root (Node): The root node of the suffix tree.
        global_end (End): End object to denote the end of all active edges.
        active_point (ActivePoint): Maintains the current active point in the suffix tree during construction.
        remainder (int): Tracks the number of suffixes yet to be inserted into the suffix tree.
        previous_node (Node or None): References the previously created internal node, if any.

    Methods:
        build_suffix_tree(): Initiates the construction of the suffix tree by processing each character in the text.
        extend_suffix_tree(i): Extends the suffix tree for the character at index "i".
    """

    def __init__(self, text):
        # append unique terminator
        self.text = text + "$"
        
        self.root = Node()
        self.root.link = self.root

        # global end for all active edges
        self.global_end = End()
        
         # initialise active point
        self.active_point = ActivePoint(self.root)
        
        self.remainder = 0
        self.previous_node = None
        self.build_suffix_tree()

    def build_suffix_tree(self):
        """
        Iterates through the input text and constructs the suffix tree by processing each character. This method 
        updates the global end and manages the number of suffixes to insert.
        """

        for i in range(len(self.text)):

            # set global end for current phase
            self.global_end.value = i

            self.remainder += 1

            # reset the previous node before processing the next character
            self.previous_node = None

            # extend suffix tree for this phase
            self.extend_suffix_tree(i)

    def extend_suffix_tree(self, i):
        """
        Extends the suffix tree for the character at index "i" in the text.

        It handles the insertion of the current character into the suffix tree based on Ukkonen's algorithm. It 
        manages the active point and performs the necessary edge creations and splits to ensure that all suffixes of the 
        input string are represented correctly in the suffix tree.

        Args:
            i (int): The index of the current character in the text.

        Process:
            - Updates the active edge based on the current character index.
            - Checks if the active edge exists. If not, it creates a new leaf edge.
            - If an active edge exists, it compares the current character with the character on the active edge.
            - If there is a mismatch, the edge is split, creating an internal node.
            - Updates the suffix link for previously created internal nodes as needed.
            - Adjusts the active point for the next iteration, handling cases where the active node is the root or has a 
              valid suffix link.
        """

        # current character to add
        char = self.text[i]

        # continue processing until all suffixes from the text have been inserted into the suffix tree
        while self.remainder > 0:
            # update active edge if needed
            self.active_point.update_active_edge(i)

            # retrieve the edge corresponding to the current character in the active edge of the active node
            edge = self.active_point.active_node.edges[ord(self.text[self.active_point.active_edge]) - ALPHABET_START]

            # rule 2: create a new leaf edge if no edge exists for the active character
            if edge is None:
                # create a new edge starting from the current index to the global end
                new_edge = Edge(i, self.global_end, i - self.remainder + 1)

                # assign the new edge to the active node's edges
                self.active_point.active_node.edges[ord(self.text[self.active_point.active_edge]) - ALPHABET_START] = new_edge

                # update the suffix link of the previous node if applicable
                if self.previous_node:
                    self.previous_node.link = self.active_point.active_node

                # reset previous_node for next iteration
                self.previous_node = None

            else:
                # rule 3: check for a match within an edge
                if self.active_point.active_length >= len(edge):

                    # move along the edge if the active length exceeds the edge length
                    self.active_point.active_edge += len(edge)
                    self.active_point.active_length -= len(edge)
                    self.active_point.active_node = edge.next
                    continue

                # rule 3 extension: showstopper
                # compare character at position (active edge start + active length)
                if self.text[edge.start + self.active_point.active_length] == char:

                    # if characters match, extend the active length
                    self.active_point.active_length += 1

                    # update the previous node's suffix link if applicable
                    if self.previous_node:
                        self.previous_node.link = self.active_point.active_node

                    # move to the next phase without further updates
                    break

                # rule 2: split edge, create internal node
                split_end = End(edge.start + self.active_point.active_length - 1)
                
                # create a new internal node
                internal_node = Node()

                # create a new edge for the current character
                new_edge = Edge(i, self.global_end, i - self.remainder + 1)
                internal_node.edges[ord(self.text[i]) - ALPHABET_START] = new_edge

                # create an internal edge for the existing edge that will be split
                internal_edge = Edge(edge.start, split_end)

                # set the next node for the internal edge
                internal_edge.next = internal_node

                # assign the internal edge to the active node's edges
                self.active_point.active_node.edges[ord(self.text[self.active_point.active_edge]) - ALPHABET_START] = internal_edge

                # adjust the start of the original edge after the split
                edge.start += self.active_point.active_length
                internal_node.edges[ord(self.text[edge.start]) - ALPHABET_START] = edge

                # update the suffix link for the previous node if applicable
                if self.previous_node:
                    self.previous_node.link = internal_node

                # set previous_node to the newly created internal node
                self.previous_node = internal_node

            # decrement the remainder count for suffixes
            self.remainder -= 1

            # adjust the active point for the next iteration
            if self.active_point.active_node == self.root and self.active_point.active_length > 0:
                self.active_point.active_length -= 1
                self.active_point.active_edge = i - self.remainder + 1
            else:
                # check if there is a valid suffix link from the current active node
                if self.active_point.active_node.link is not None:
                    # follow the suffix link to the next node
                    self.active_point.active_node = self.active_point.active_node.link
                else:
                    # if there is no suffix link, reset to the root node
                    self.active_point.active_node = self.root

    def suffix_tree_to_suffix_array(self):
        """
        Converts the constructed suffix tree into a suffix array.

        The suffix array is created by performing a depth first traversal of the suffix tree, collecting the indices 
        of the leaves, which represent the starting positions of the suffixes in the original string.

        Returns:
            list [int]: A list representing the starting indices of suffixes in sorted order.
        """

        suffix_array = []

        # traverse the suffix tree starting from the root
        self.traverse(self.root, suffix_array)

        return suffix_array

    def traverse(self, current_node, suffix_array):
        """
        Traverse the suffix tree starting from the given node and collect the suffix indices from the leaf nodes.

        Args:
            current_node (Node): The node from which to start the traversal.
            suffix_array (list): The list to which suffix indices will be appended.

        Returns:
            list: The updated suffix array containing indices of suffixes.
        """

        # check if current node exists
        if current_node is not None:

            # traverse all edges from the current node
            for edge in current_node.edges:
                if edge is not None:
                    # recursively traverse the next node if it exists
                    if edge.next is not None:
                        self.traverse(edge.next, suffix_array)

                    # if it's a leaf node, append the suffix index
                    else:
                        suffix_array.append(edge.suffix_id)

        return suffix_array
    
if __name__ == "__main__":
    text = "banana"
    ukkonen = Ukkonen(text)
    suffix_array = ukkonen.suffix_tree_to_suffix_array()
    print(suffix_array)