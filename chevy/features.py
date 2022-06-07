from __future__ import annotations
import operator
from functools import cached_property
from typing import List, Dict, Tuple

import chess
import chess.pgn
import numpy as np
from cachetools import cachedmethod, LRUCache
from scipy.ndimage import label

from chevy.utils import count_bits


class BoardFeaturesBase:
    CENTRAL_SQUARES = {
        27, 28, 35, 36
    }

    def __init__(self, board: chess.Board, color: chess.Color = chess.WHITE):
        self.board = board
        self.color = color

    @cached_property
    def mobility_map(self) -> Dict[chess.Square, List[chess.Square]]:
        board = self.board.copy()
        # hack to overcome no legal moves when in check
        # we remove our king from board to eliminate effect of
        # potential opponents checks, instead we place a pawn on that square
        # so it still blocks movement of our pieces

        our_king = board.king(self.color)
        board.remove_piece_at(our_king)
        board.set_piece_at(our_king, chess.Piece(chess.PAWN, self.color))
        # hack to overcome no legal moves when opponent to move
        if board.turn != self.color:
            board.turn = not board.turn

        result: dict = dict()
        for m in list(board.legal_moves):
            result[m.from_square] = result.get(m.from_square, list()) + (
                [m.to_square] if m.from_square != our_king else []
            )

        # here we fix previously edited board - we place king on the board again
        # and only then look at its legal moves
        # (now any checks are again respected)
        board.set_piece_at(our_king, chess.Piece(chess.KING, self.color))
        result[our_king] = [
            m.to_square for m in board.legal_moves if
            m.from_square == our_king
        ]

        return result

    @cached_property
    def our_pieces_count(self) -> int:
        return len(self._all_our_pieces_square_set)

    @cached_property
    def their_pieces_count(self) -> int:
        return len(self._all_their_pieces_square_set)

    @cached_property
    def all_pieces_count(self) -> int:
        return self.our_pieces_count + self.their_pieces_count

    @cached_property
    def _all_our_pieces_square_set(self) -> chess.SquareSet:
        return self._get_all_pieces_square_set(self.color)

    @cached_property
    def _all_their_pieces_square_set(self) -> chess.SquareSet:
        return self._get_all_pieces_square_set(not self.color)

    def _get_all_pieces_square_set(self, color: chess.Color) -> chess.SquareSet:
        all_pieces = chess.SquareSet()
        for piece in chess.PIECE_TYPES:
            all_pieces |= self.board.pieces(
                piece,
                color=color
            )
        return all_pieces

    def _get_mobility_count_vector(self, piece) -> List[int]:
        return sorted([
            len(self.mobility_map.get(i, list()))
            for i in self.board.pieces(piece, color=self.color)
        ])

    def _are_pieces_connected(self, piece: chess.PieceType) -> bool:
        mutual_attack_mask = chess.SquareSet()
        for i in self.board.pieces(piece, self.color):
            mutual_attack_mask = mutual_attack_mask.union(
                self.board.attacks(i)
            )

        return count_bits(
            mutual_attack_mask.intersection(
                self.board.pieces(piece, self.color)
            ).mask
        ) > 1

    def _get_pieces_centrality(self, piece: chess.PieceType,
                               color: chess.Color) -> List[int]:
        return sorted([
            3 - min(
                7 - (p // 8), p // 8, 7 - p % 8, p % 8
            )
            for p in self.board.pieces(piece, color)
        ])


class BoardFeatures(BoardFeaturesBase):

    @cached_property
    def fianchetto_queen(self) -> bool:

        bishop_at = 9 + (0 if self.color == chess.WHITE else (5 * 8))
        pawn1_at = 8 + (0 if self.color == chess.WHITE else (5 * 8))
        pawn2_at = 17 + (0 if self.color == chess.WHITE else (3 * 8))

        bishop_placed_properly = (
                self.board.piece_at(bishop_at) ==
                chess.Piece(color=self.color, piece_type=chess.BISHOP)
        )

        pawn1_places_properly = (
                self.board.piece_at(pawn1_at) ==
                chess.Piece(color=self.color, piece_type=chess.PAWN)
        )

        pawn2_places_properly = (
                self.board.piece_at(pawn2_at) ==
                chess.Piece(color=self.color, piece_type=chess.PAWN)
        )

        return (
                bishop_placed_properly and
                pawn1_places_properly and
                pawn2_places_properly
        )

    @cached_property
    def fianchetto_king(self) -> bool:
        bishop_at = 14 + (0 if self.color == chess.WHITE else (5 * 8))
        pawn1_at = 15 + (0 if self.color == chess.WHITE else (5 * 8))
        pawn2_at = 22 + (0 if self.color == chess.WHITE else (3 * 8))

        bishop_placed_properly = (
                self.board.piece_at(bishop_at) ==
                chess.Piece(color=self.color, piece_type=chess.BISHOP)
        )

        pawn1_places_properly = (
                self.board.piece_at(pawn1_at) ==
                chess.Piece(color=self.color, piece_type=chess.PAWN)
        )

        pawn2_places_properly = (
                self.board.piece_at(pawn2_at) ==
                chess.Piece(color=self.color, piece_type=chess.PAWN)
        )

        return (
                bishop_placed_properly and
                pawn1_places_properly and
                pawn2_places_properly
        )

    @cached_property
    def connectivity(self) -> int:
        c = 0
        for p in self._all_our_pieces_square_set:
            c += len(
                self.board.attacks(p).intersection(
                    self._all_our_pieces_square_set)
            )
        return c

    @cached_property
    def material_vector_count(self) -> List[int]:
        return [
            count_bits(self.board.pieces(chess.PAWN, self.color).mask),
            count_bits(self.board.pieces(chess.KNIGHT, self.color).mask),
            count_bits(self.board.pieces(chess.BISHOP, self.color).mask),
            count_bits(self.board.pieces(chess.ROOK, self.color).mask),
            count_bits(self.board.pieces(chess.QUEEN, self.color).mask),
            count_bits(self.board.pieces(chess.KING, self.color).mask),
        ]

    @cached_property
    def connected_rooks(self) -> bool:
        return self._are_pieces_connected(chess.ROOK)

    @cached_property
    def connected_knights(self) -> bool:
        return self._are_pieces_connected(chess.KNIGHT)

    @cached_property
    def bishop_pair(self) -> bool:
        return len(self.bishops_mobility) > 1

    @cached_property
    def bishops_mobility(self) -> List[int]:
        return self._get_mobility_count_vector(chess.BISHOP)

    @cached_property
    def knights_mobility(self) -> List[int]:
        return self._get_mobility_count_vector(chess.KNIGHT)

    @cached_property
    def rooks_mobility(self) -> List[int]:
        return self._get_mobility_count_vector(chess.ROOK)

    @cached_property
    def queens_mobility(self) -> List[int]:
        return self._get_mobility_count_vector(chess.QUEEN)

    @cached_property
    def pawn_mobility_sum(self) -> int:
        return sum(self._get_mobility_count_vector(chess.PAWN))

    @cached_property
    def knights_centrality(self) -> List[int]:
        return self._get_pieces_centrality(chess.KNIGHT, self.color)

    @cached_property
    def bishops_centrality(self) -> List[int]:
        return self._get_pieces_centrality(chess.BISHOP, self.color)

    @cached_property
    def queens_centrality(self) -> List[int]:
        return self._get_pieces_centrality(chess.QUEEN, self.color)

    @cached_property
    def open_files_rooks_count(self) -> int:
        our_pawns_files = {
            chess.square_file(p) for p in
            self.board.pieces(chess.PAWN, self.color)
        }
        their_pawns_files = {
            chess.square_file(p) for p in
            self.board.pieces(chess.PAWN, not self.color)
        }
        return len([
            p for p in self.board.pieces(chess.ROOK, self.color) if
            (chess.square_file(p) not in our_pawns_files) and
            (chess.square_file(p) not in their_pawns_files)
        ])

    @cached_property
    def pins_vector(self) -> List[int]:
        result = [0] * len(chess.PIECE_TYPES)
        for p in self._all_our_pieces_square_set:
            piece = self.board.piece_at(p)
            if self.board.is_pinned(self.color, p):
                result[piece.piece_type - 1] += 1
        return result

    @cached_property
    def legal_moves_count(self) -> int:
        return len(list(self.board.legal_moves))

    @cached_property
    def threats_vector(self) -> List[int]:
        result_vector_checks = [0] * len(chess.PIECE_TYPES)
        result_vector_checkmates = [0] * len(chess.PIECE_TYPES)
        result_vector_stalemates = [0] * len(chess.PIECE_TYPES)
        board = self.board
        if self.board.turn != self.color:
            if not self.board.is_check():
                board = self.board.copy()
                board.turn = not board.turn
            else:
                return (
                        result_vector_checks + result_vector_checkmates +
                        result_vector_stalemates
                )
        for m in board.legal_moves:
            b_c = board.copy()
            b_c.push(m)
            p = self.board.piece_at(m.from_square)
            result_vector_checks[p.piece_type - 1] += b_c.is_check()
            result_vector_checkmates[p.piece_type - 1] += b_c.is_checkmate()
            result_vector_stalemates[p.piece_type - 1] += b_c.is_stalemate()

        return (
                result_vector_checks + result_vector_checkmates +
                result_vector_stalemates
        )


class KingSafety(BoardFeaturesBase):

    def __init__(self, board: chess.Board, color: chess.Color):
        super().__init__(board, color)
        self._cache: LRUCache = LRUCache(
            maxsize=8)  # most likely 1 is good enough

    KING_PROXIMITY_OFFSET_RING_1 = [
        [1, 0], [1, -1], [1, 1], [-1, -1],
        [-1, 0], [-1, 1], [0, 1], [0, -1]
    ]

    KING_PROXIMITY_OFFSET_RING_2 = [
        [2, -2], [2, -1], [1, 2], [2, 1], [-2, -2], [-2, -1], [-1, -2], [-2, 1],
        [2, 0], [1, -2], [-1, 2], [-2, 0], [0, 2], [2, 2], [-2, 2], [0, -2]
    ]

    @cached_property
    def checked(self) -> bool:
        return self.board.turn == self.color and self.board.is_check()

    @cached_property
    def castling_rights(self) -> bool:
        return self.board.has_castling_rights(self.color)

    @cached_property
    def king_attackers_looking_at_ring_1(self) -> List[int]:
        attackers_looking_at_ring, _, _, _ = self.__get_ring_features(
            self._king_ring_1
        )
        return attackers_looking_at_ring

    @cached_property
    def king_attackers_at_ring_1(self) -> List[int]:
        _, _, attackers_at_ring, _ = self.__get_ring_features(
            self._king_ring_1
        )
        return attackers_at_ring

    @cached_property
    def king_defenders_at_ring_1(self) -> List[int]:
        _, _, _, defenders_at_ring = self.__get_ring_features(
            self._king_ring_1
        )
        return defenders_at_ring

    @cached_property
    def king_defenders_looking_at_ring_1(self) -> List[int]:
        _, defenders_looking_at_ring, _, _ = self.__get_ring_features(
            self._king_ring_1
        )
        return defenders_looking_at_ring

    @cached_property
    def king_attackers_looking_at_ring_2(self) -> List[int]:
        attackers_looking_at_ring, _, _, _ = self.__get_ring_features(
            self._king_ring_2
        )
        return attackers_looking_at_ring

    @cached_property
    def king_attackers_at_ring_2(self) -> List[int]:
        _, _, attackers_at_ring, _ = self.__get_ring_features(
            self._king_ring_2
        )
        return attackers_at_ring

    @cached_property
    def king_defenders_at_ring_2(self) -> List[int]:
        _, _, _, defenders_at_ring = self.__get_ring_features(
            self._king_ring_2
        )
        return defenders_at_ring

    @cached_property
    def king_defenders_looking_at_ring_2(self) -> List[int]:
        _, defenders_looking_at_ring, _, _ = self.__get_ring_features(
            self._king_ring_2
        )
        return defenders_looking_at_ring

    @cached_property
    def king_mobility(self) -> int:
        return self._get_mobility_count_vector(chess.KING).pop()

    @cached_property
    def king_centrality(self) -> int:
        return self._get_pieces_centrality(chess.KING, self.color).pop()

    @cached_property
    def _king_ring_1(self) -> chess.SquareSet:
        return self.__king_ring(self.KING_PROXIMITY_OFFSET_RING_1)

    @cached_property
    def _king_ring_2(self) -> chess.SquareSet:
        return self.__king_ring(self.KING_PROXIMITY_OFFSET_RING_2)

    def __king_ring(self, king_ring_offset) -> chess.SquareSet:
        n = self.board.pieces(chess.KING, self.color).pop()
        x, y = n // 8, n % 8
        squares = chess.SquareSet()
        for a, b in king_ring_offset:
            if (8 > x + a >= 0) and (0 <= y + b < 8):
                squares.add(chess.Square((x + a) * 8 + y + b))
        return squares

    @cachedmethod(operator.attrgetter('_cache'),
                  key=lambda self, x: x.mask)
    def __get_ring_features(self, king_ring) \
            -> Tuple[List[int], List[int], List[int], List[int]]:
        attackers_looking_at_ring = [0] * len(chess.PIECE_TYPES)
        defenders_looking_at_ring = [0] * len(chess.PIECE_TYPES)
        attackers_at_ring = [0] * len(chess.PIECE_TYPES)
        defenders_at_ring = [0] * len(chess.PIECE_TYPES)

        attackers_looking_at_ring_seen = set()
        defenders_looking_at_ring_seen = set()
        for sq in king_ring:

            p = self.board.piece_at(sq)

            if p:
                if p.color == (not self.color):
                    attackers_at_ring[p.piece_type - 1] += 1
                else:
                    defenders_at_ring[p.piece_type - 1] += 1

            attackers = self.board.attackers(
                color=not self.color,
                square=sq
            )

            defenders = self.board.attackers(
                color=self.color,
                square=sq
            )

            if attackers:
                for attacker_square in attackers:
                    piece = self.board.piece_at(attacker_square)
                    if piece and attacker_square not in attackers_looking_at_ring_seen:
                        attackers_looking_at_ring[piece.piece_type - 1] += 1
                        attackers_looking_at_ring_seen.add(attacker_square)

            if defenders:
                for defender_square in defenders:
                    piece = self.board.piece_at(defender_square)
                    if piece and defender_square not in defenders_looking_at_ring_seen:
                        defenders_looking_at_ring[piece.piece_type - 1] += 1
                        defenders_looking_at_ring_seen.add(defender_square)

        return (
            attackers_looking_at_ring, defenders_looking_at_ring,
            attackers_at_ring, defenders_at_ring
        )


class PawnStructure(BoardFeaturesBase):

    def __init__(self, board: chess.Board, color: chess.Color):
        super().__init__(board, color)
        self.pawns_at_file = [0] * 8
        for p in self.board.pieces(chess.PAWN, color):
            self.pawns_at_file[chess.square_file(p)] += 1

    @cached_property
    def central_pawns(self) -> int:
        return len(
            [
                0 for p in self.board.pieces(chess.PAWN, self.color) if
                p in self.CENTRAL_SQUARES
            ]
        )

    @cached_property
    def pawns_advancements(self) -> List[int]:
        files = [-1] * 8
        for p in self.board.pieces(chess.PAWN, self.color):
            pawn_file = chess.square_file(p)
            files[pawn_file] = max(files[pawn_file], p // 8)
        return files

    @cached_property
    def blocked_pawns(self) -> int:
        c = 0
        for p in self.board.pieces(chess.PAWN, color=self.color):
            opposite_piece = self.board.piece_at(
                p + (8 if self.color == chess.WHITE else -8))
            if (self.mobility_map.get(p) is None and  # no mobility
                    opposite_piece and  # piece in front of current square
                    opposite_piece.color == (not self.color)  # opposite color
            ):
                c += 1
        return c

    @cached_property
    def isolated_pawns(self) -> int:
        isolated = 0
        if self.pawns_at_file[0] > 0 and self.pawns_at_file[1] == 0:
            isolated += self.pawns_at_file[0]  # or 1 ?

        if self.pawns_at_file[7] > 0 and self.pawns_at_file[6] == 0:
            isolated += self.pawns_at_file[7]  # or 1 ?

        for i in [1, 2, 3, 4, 5, 6]:
            if self.pawns_at_file[i] > 0 and self.pawns_at_file[
                i - 1] == 0 and \
                    self.pawns_at_file[i + 1] == 0:
                isolated += self.pawns_at_file[i]  # or 1 ?
        return isolated

    @cached_property
    def double_pawns(self) -> int:
        double_pawns = 0
        for p in self.pawns_at_file:
            if p > 1:
                double_pawns += 1
        return double_pawns

    @cached_property
    def passed_pawns(self) -> int:
        # always white perspective
        b = self.board
        if self.color == chess.BLACK:
            b = self.board.mirror()

        m = np.zeros((8, 8))
        for p in b.pieces(chess.PAWN, chess.WHITE):
            x, y = p // 8, p % 8
            m[x][y] = 1

        for p in b.pieces(chess.PAWN, chess.BLACK):
            x, y = p // 8, p % 8
            m[x][y] = -1

        s = chess.SquareSet()
        for x, y in zip(*np.where(m == 1)):
            if not (any(m[x:, y] == -1) or (
                    y < 7 and any(m[x:, (y + 1)] == -1)) or (
                            y > 0 and any(m[x:, (y - 1)] == -1))):
                s.add(x * 8 + y)
        return len(s)

    @cached_property
    def pawn_islands(self) -> int:
        m = np.zeros((8, 8))
        for p in self.board.pieces(chess.PAWN, self.color):
            x, y = p // 8, p % 8
            m[x][y] = 1
        _, c = label(m, structure=[[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        return c
