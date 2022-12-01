"""A circular genome for simulating transposable elements."""

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod,
)


class Genome(ABC):
    """Representation of a circular enome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    nucleotide: list[str]
    active_TE: dict[int, int]
    te_id: int

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.nucleotide = ["-"] * n
        self.active_TE = {}
        self.te_id = 1

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        if self.nucleotide[pos] in self.active_TE:
            del self.active_TE[self.nucleotide[pos]]

        te_id, self.te_id = self.te_id, self.te_id + 1
        self.active_TE[te_id] = length
        self.nucleotide[pos:pos] = [te_id] * length

        return te_id

    def copy_te(self, te_id: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        if te_id not in self.active_TE:
            return None

        pos = self.nucleotide.index(te_id)
        length = self.active_TE[te_id]

        # modulo to fix out of boundsness.
        return self.insert_te((pos + offset) % len(self.nucleotide), length)

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        if te in self.active_TE:
            del self.active_TE[te]

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""

        return list(self.active_TE.keys())

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.nucleotide)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """

        return "".join(
            a if a == "-" else "A" if a in self.active_TE else "x"
            for a in self.nucleotide
        )


class Node:
    def __init__(self, te, next=None, prev=None):
        self.te = te
        self.next = next
        self.te_id = 0
        # self.prev = prev


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    active_TE = dict
    te_id = int

    def __init__(self, n: int):
        self.active_TE = {}
        self.next_TE_id = 1

        # init LL Head
        self.head = Node(0)
        # self.head.prev = self.head
        # seriously dont use below, this kills the program.
        # self.head.next = self.head

        # make genome
        for _ in range(n):
            self.insert(0)
        self.length = n
        # burde kunne "cirkuleres" hvis tail bare peger tilbage på head.

    # burde nok ikke gøres uden at lave stops så while loops.

    def insert(self, te):
        insert = Node(te)
        # no need to head check as head will allways start as 0, i hope.
        current = self.head
        while current.next:
            current = current.next
        current.next = insert

    # inserts after the given node.
    def insert_in(self, node, te):
        insert = Node(te)
        insert.next, node.next = node.next, insert
        return insert

    def insert_te(self, position: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """

        currentNode = self.head
        position = position % self.length
        TE_ID = self.next_TE_id
        # path to node before insertion
        for _ in range(0, position - 1):
            currentNode = currentNode.next
        insertionNode = currentNode
        # check for TE and disable it
        currentNode = currentNode.next
        if currentNode.te == 1:
            self.disable_te(currentNode.te_id)

        # insert the TE
        currentNode = insertionNode
        for i in range(length):
            currentNode: Node = self.insert_in(currentNode, 1)  # 1 for active TE
            currentNode.te_id = TE_ID
            if i == 0:
                self.active_TE[TE_ID] = [currentNode, length]

        # set fields for next TE
        self.next_TE_id += 1
        self.length += length
        return TE_ID

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """

        if te not in self.active_TE:
            return None

        pos = 0

        currentNode = self.head
        # find the first node and position of it, in the target TE.
        for _ in range(self.length):
            if currentNode.te_id == te:
                break
            currentNode = currentNode.next
            pos += 1

        TE_ID = self.next_TE_id
        # path to node before insertion
        pos = pos + (offset % self.length)
        currentNode = self.head

        for _ in range(0, pos - 1):
            currentNode = currentNode.next
        insertionNode = currentNode
        length: int = self.active_TE[te][1]
        # check for TE and disable it
        currentNode = currentNode.next
        if currentNode.te == 1:
            self.disable_te(currentNode.te_id)

        # insert the TE
        currentNode = insertionNode
        for i in range(length):
            currentNode: Node = self.insert_in(currentNode, 1)  # 1 for active TE
            currentNode.te_id = TE_ID
            if i == 0:
                self.active_TE[TE_ID] = [currentNode, length]

        # set fields for next TE
        self.next_TE_id += 1
        self.length += length
        return TE_ID

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """

        currentNode: Node = self.active_TE[te][0]
        length: int = self.active_TE[te][1]
        for _ in range(length):
            currentNode.te = 2
            currentNode = currentNode.next

        del self.active_TE[te]

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return list(self.active_TE.keys())

    def __len__(self) -> int:
        """Current length of the genome."""

        last = self.head
        i = 0
        while last.next:
            last = last.next
            i += 1
        return i

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        returnString = ""
        last = self.head
        while last.next:
            returnString += "A" if last.te == 1 else "x" if last.te == 2 else "-"
            last = last.next
        return returnString


# genome = LinkedListGenome(10)
# print(genome.__str__)
