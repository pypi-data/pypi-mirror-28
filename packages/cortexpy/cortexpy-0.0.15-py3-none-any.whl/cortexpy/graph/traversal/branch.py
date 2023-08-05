import attr

from cortexpy import graph
from cortexpy.graph.serializer import SERIALIZER_GRAPH
from cortexpy.constants import EdgeTraversalOrientation


class KmerStringAlreadySeen(Exception):
    pass


@attr.s(slots=True)
class Branch(object):
    ra_parser = attr.ib()
    traversal_color = attr.ib(0)
    graph = attr.ib(attr.Factory(SERIALIZER_GRAPH))
    kmer = attr.ib(init=False, default=None)
    kmer_string = attr.ib(init=False)
    prev_kmer = attr.ib(init=False)
    prev_kmer_string = attr.ib(init=False)
    orientation = attr.ib(init=False)
    parent_graph = attr.ib(init=False)

    def traverse_from(self, kmer_string, *,
                      orientation=EdgeTraversalOrientation.original,
                      parent_graph=None):
        if parent_graph is None:
            parent_graph = set()
        self.parent_graph = parent_graph
        self.graph = SERIALIZER_GRAPH()
        self.kmer_string = first_kmer_string = kmer_string
        self.orientation = orientation
        self.prev_kmer_string = None

        try:
            self._get_kmer_and_add_kmer_string_to_graph()
        except KmerStringAlreadySeen:
            return TraversedBranch(self.graph, orientation=self.orientation)

        while True:
            oriented_edge_set = self.kmer.edges[self.traversal_color].oriented(self.orientation)
            if (
                            self._get_num_neighbors(oriented_edge_set) != 1
                    or self._get_num_neighbors(oriented_edge_set.other_orientation()) > 1
            ):
                break
            try:
                self._add_next_kmer_string_to_graph_and_get_next_kmer(oriented_edge_set)
                self._add_edges()
            except KmerStringAlreadySeen:
                break

        reverse_neighbor_kmer_strings = set(
            self._get_neighbors(oriented_edge_set.other_orientation()))
        if self.prev_kmer_string is not None:
            reverse_neighbor_kmer_strings.remove(self.prev_kmer_string)
        return TraversedBranch(self.graph,
                               orientation=self.orientation,
                               first_kmer_string=first_kmer_string,
                               last_kmer_string=self.kmer_string,
                               neighbor_kmer_strings=self._get_neighbors(oriented_edge_set),
                               reverse_neighbor_kmer_strings=list(reverse_neighbor_kmer_strings))

    def _get_num_neighbors(self, oriented_edge_set):
        return oriented_edge_set.num_neighbor(self.kmer_string)

    def _get_neighbors(self, oriented_edge_set):
        return oriented_edge_set.neighbor_kmer_strings(self.kmer_string)

    def _add_next_kmer_string_to_graph_and_get_next_kmer(self, oriented_edge_set):
        next_kmer_string = oriented_edge_set.neighbor_kmer_strings(self.kmer_string)[0]
        prev_kmer_string = self.kmer_string
        try:
            self.kmer_string = next_kmer_string
            self._get_kmer_and_add_kmer_string_to_graph()
        except KmerStringAlreadySeen:
            self.kmer_string = prev_kmer_string
            raise
        self.prev_kmer_string = prev_kmer_string

    def _add_edges(self):
        first, second = (self.prev_kmer_string, self.prev_kmer), (self.kmer_string, self.kmer)
        if self.orientation == EdgeTraversalOrientation.reverse:
            first, second = second, first
        graph_interactor = graph.Interactor(self.graph, first[1].colors)
        graph_interactor.add_edge_to_graph_for_kmer_pair(first[1], second[1], first[0], second[0])

    def _get_kmer(self):
        if self.kmer_string in self.graph or self.kmer_string in self.parent_graph:
            raise KmerStringAlreadySeen
        prev_kmer = self.kmer
        self.kmer = self.ra_parser.get_kmer_for_string(self.kmer_string)
        self.prev_kmer = prev_kmer

    def _get_kmer_and_add_kmer_string_to_graph(self):
        self._get_kmer()
        self.graph.add_node(self.kmer_string, kmer=self.kmer)


@attr.s(slots=True)
class TraversedBranch(object):
    graph = attr.ib()
    orientation = attr.ib()
    first_kmer_string = attr.ib(None)
    last_kmer_string = attr.ib(None)
    neighbor_kmer_strings = attr.ib(attr.Factory(list))
    reverse_neighbor_kmer_strings = attr.ib(attr.Factory(list))
