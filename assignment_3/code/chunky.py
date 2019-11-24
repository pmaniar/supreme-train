from functools import reduce
from typing import List, Dict, Tuple


class Chunky(object):
    """ Data Structure to manage chunks."""

    # TODO: fix data structure. Not the most efficient way to do this.

    @staticmethod
    def create_Chunky(data: Dict[str, Dict[int, List[int]]]) -> object:
        """ Creates a Chunky object with pre-existing data.

        Args:
            data: Data format identical to that of self.files

        Returns:
            A Chunky object with data pre-populated.
        """
        c = Chunky()
        c.files = data
        c.peers = max(
            map(lambda x: max(map(lambda y: max(y, default=0), x.values()), default=0),
                data.values()), default=0)
        return c

    def __init__(self):
        """ Constructor.

        """
        # Map from Files -> (Map from Chunks -> List[peer ID's with specific chunk from file]
        # {
        #     "file1": {
        #         1: [1, 2, 5],  # User 1,2,5 have Chunk 1
        #         2: [1],  # User 1 has Chunk 2
        #         ...
        #     },
        #     "file2": {
        #         ...
        #     },
        #     ...
        # }

        # Dict[str, Dict[int, List[int]]]
        self.files = {}
        self.peers = 0

    def add_chunk_to_peer(self, peerId: int, filename: str, chunkId: int) -> None:
        """ Assigns that a peer has a certain chunk from a file.

        Args:
            peerId: The Id of the peer.
            filename: The file corresponding file that has been acquired.
            chunkId: The Id of the chunk in the filename that has been acquired.
        """
        self.files[filename][chunkId].append(peerId)

    def remove_peer(self, peerId: int) -> None:
        """ Removes a peer from Chunky.

        Args:
            peerId: The peer to remove from Chunky.
        """
        for chunks in self.files.values():
            for chunk in chunks.values():
                if peerId in chunk:
                    chunk.remove(peerId)

    def add_file(self, peerId: int, filename: str, chunks: int) -> None:
        """ Adds a new file to chunky.

        It is assumed filename conflicts will not occur.

        Args:
            peerId: The Id of the peer with the file.
            filename: The name of the file.
            chunks: The number of chunks the file has.
        """
        self.files[filename] = dict([(i, peerId) for i in range(chunks)])

    def has_all_files(self, files: Dict[str, List[int]]) -> bool:
        """ Checks if the given files contain all those in Chunky.(i.e.
            chunky \subseteq files)

        Args:
            files: A mapping of files to a list of chunks from that file.

        Returns:
            True if all files in Chunky appear in the files, False otherwise.
        """
        for f in self.files.keys():
            if len(set(self.files[f].keys()) - set(files.get(f, []))) > 0:
                return False

        return True

    def get_next_peer(self, files: Dict[str, List[int]]) -> Tuple[int, str, List[int]]:
        """ Calculates which file and peer the peer with the files should contact next.

        Args:
            files: A mapping of files to a list of chunks from that file that a peer has.

        Returns:
            A tuple containing the following:
                * The id of the peer to contact.
                * The file to ask for.
                * The List of chunks to ask for.

            Return the next peer to connect to, which file and chunks should be asked for.
        """
        for f in self.files.keys():
            if len(set(self.files[f].keys()) - set(files.get(f, []))) > 0:
                users = list(reduce(lambda x, y: set(x).intersection(set(y)),
                                    self.files[f].values()))
                return users[0], f, self.files[f][users[0]]
