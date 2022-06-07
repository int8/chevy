import chess

from chevy.features import BoardFeatures


def test_fianchetto():
    fen = "rnbqk1nr/ppppppbp/6p1/8/8/6P1/PPPPPPBP/RNBQK1NR w KQkq - 0 6"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.fianchetto_king
    assert not board_features.fianchetto_queen
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.fianchetto_king
    assert not board_features.fianchetto_queen

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.fianchetto_king
    assert not board_features.fianchetto_queen
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.fianchetto_king
    assert not board_features.fianchetto_queen

    fen = "rn1qk1nr/pbppppbp/1p4p1/8/8/1P4P1/PBPPPPBP/RN1QK1NR w KQkq - 0 6"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.fianchetto_king
    assert board_features.fianchetto_queen
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.fianchetto_king
    assert board_features.fianchetto_queen

    fen = "rn1qk1nr/p1pppp1p/bp4pb/8/8/1PB2BP1/P1PPPP1P/RN1QK1NR w KQkq - 0 6"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.fianchetto_king
    assert not board_features.fianchetto_queen
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.fianchetto_king
    assert not board_features.fianchetto_queen


def test_pins_vector():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pins_vector == [0] * 6
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pins_vector == [0] * 6

    fen = "r2qk1nr/ppp2ppp/2n1b3/1B2p3/1b2P3/2NP4/PPP2PPP/RNBQK2R w KQkq - 0 9"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pins_vector == [0, 1, 0, 0, 0, 0]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pins_vector == [0, 1, 0, 0, 0, 0]

    fen = "r2qk1nr/pppb1ppp/2n5/1B2p3/1b2P3/2NP4/PPP2PPP/RNBQK2R w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pins_vector == [0, 1, 0, 0, 0, 0]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pins_vector == [0, 0, 0, 0, 0, 0]

    fen = "r2qk1nr/pppb1ppp/2n5/1B2p2Q/1b2P3/2NP4/PPP2PPP/RNB1K2R w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pins_vector == [0, 1, 0, 0, 0, 0]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pins_vector == [1, 0, 0, 0, 0, 0]


def test_threats_vector():
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] * 3
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == [0] * 18
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == [0] * 18

    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == [0] * 18
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == [0] * 18

    fen = "r3k1n1/pppp1ppp/1b1n4/1q2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == [0] * 18
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == [0, 1, 2, 1, 3, 0] + [0] * 12

    fen = "1Qn1k1n1/1ppp1ppp/1b6/3qpK2/2b1P1r1/8/P5PP/RNB2BNR w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == [0, 0, 0, 0, 1, 0] + [0] * 12
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [1, 2, 0, 2, 2, 0] + [0, 0, 0, 0, 2, 0] + [0] * 6
    )

    fen = "1Qn1k1n1/1ppp1pp1/1b6/3qpK1p/2b1P1r1/8/P5PP/RNB2BNR w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == [0, 0, 0, 0, 1, 0] + [0] * 12
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [1, 2, 0, 2, 2, 0] + [1, 1, 0, 0, 2, 0] + [0] * 6
    )

    fen = "1Qn1k1n1/1ppp1ppN/1b6/3qpK1p/2b1P1r1/B7/P5PP/R4BNR w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0, 1, 0, 0, 1, 0] + [0, 0, 0, 0, 1, 0] + [0] * 6
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [1, 2, 0, 2, 2, 0] + [1, 1, 0, 0, 2, 0] + [0] * 6
    )

    fen = "1Qn1k1n1/1ppp1ppN/1b6/3qpK1p/2B1P1r1/B7/P5PP/R5NR w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0, 1, 0, 0, 1, 0] + [0, 0, 0, 0, 1, 0] + [0] * 6
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [1, 2, 0, 2, 2, 0] + [1, 1, 0, 0, 1, 0] + [0] * 6
    )

    fen = "3k4/8/3K4/8/8/8/8/7R w - - 0 100"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            ([0, 0, 0, 1, 0, 0] * 2) + [0] * 6
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == [0] * 18

    fen = "4k3/8/3K4/8/8/8/8/7R w - - 0 100"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0, 0, 0, 2, 0, 0] + [0] * 12
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == [0] * 18

    fen = "4k3/8/3K4/8/8/8/B7/7R w - - 0 100"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0, 0, 1, 2, 0, 0] + [0, 0, 0, 1, 0, 0] + [0] * 6
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == [0] * 18

    fen = "1rkr4/1nbn4/B7/5N2/8/8/2RK4/8 w - - 0 100"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0, 2, 1, 1, 0, 0] + [0, 2, 0, 0, 0, 0] + [0] * 6
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [0, 5, 0, 0, 0, 0] + [0] * 12
    )

    fen = "3K4/8/3k4/8/8/3q4/8/8 b - - 0 100"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0] * 18
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [0, 0, 0, 0, 0, 4] + [0] * 12
    )

    fen = "8/8/3q4/8/3k4/8/3p4/3K4 b - - 0 100"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.threats_vector == (
            [0] * 18
    )
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.threats_vector == (
            [0, 0, 0, 0, 0, 0] + [0] * 6 + [0, 0, 0, 0, 0, 1]
    )


def test_queen_mobility():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_mobility == [0]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_mobility == [0]

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_mobility == []
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_mobility == [0]

    fen = "rnbqkbnr/ppp2ppp/4p3/3p4/3P4/2N5/PPP1PPPP/R1BQKBNR w KQkq - 0 4"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_mobility == [2]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_mobility == [6]

    fen = "5rk1/r5pp/1b1qp2n/PP1p4/3P4/8/2BNKPPP/2RQN3 w - - 0 30"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_mobility == [0]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_mobility == [13]


def test_pawn_mobility_sum():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pawn_mobility_sum == 16
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pawn_mobility_sum == 16

    fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pawn_mobility_sum == 14
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pawn_mobility_sum == 14

    fen = "rnbqkbnr/8/1p1p1p1p/pPpPpPpP/P1P1P1P1/8/8/RNBQKBNR w KQkq - 0 16"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pawn_mobility_sum == 0
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pawn_mobility_sum == 0

    fen = "r2qkb2/8/bpnpnprp/pPpPpPpP/P1PQP1P1/8/8/RNB1KBNR w KQq - 0 16"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pawn_mobility_sum == 7
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pawn_mobility_sum == 2

    fen = "r2qkb2/8/bpnpnprp/p1p1p1p1/8/8/8/RNBQKBNR w KQq - 0 16"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.pawn_mobility_sum == 0
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.pawn_mobility_sum == 8


def test_pieces_count():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.our_pieces_count == 16
    assert board_features.their_pieces_count == 16
    assert board_features.all_pieces_count == 32
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.our_pieces_count == 16
    assert board_features.their_pieces_count == 16
    assert board_features.all_pieces_count == 32

    # https://lichess.org/editor/2r3k1/7R/6PK/6P1/8/8/8/8_b_-_-_6_73
    fen = "2r3k1/7R/6PK/6P1/8/8/8/8 b - - 6 73"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.our_pieces_count == 4
    assert board_features.their_pieces_count == 2
    assert board_features.all_pieces_count == 6
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.our_pieces_count == 2
    assert board_features.their_pieces_count == 4
    assert board_features.all_pieces_count == 6

    # https://lichess.org/editor/r1b2r2/p2pp2p/5k2/q1p1N3/2pnPPQ1/2N5/PPPP2PP/R1B2RK1_w_-_-_2_14
    fen = "r1b2r2/p2pp2p/5k2/q1p1N3/2pnPPQ1/2N5/PPPP2PP/R1B2RK1 w - - 2 14"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.our_pieces_count == 15
    assert board_features.their_pieces_count == 12
    assert board_features.all_pieces_count == 27
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.our_pieces_count == 12
    assert board_features.their_pieces_count == 15
    assert board_features.all_pieces_count == 27

    # https://lichess.org/editor/1kr5/R2K4/R7/4q3/8/8/8/8_b_-_-_1_31
    fen = "1kr5/R2K4/R7/4q3/8/8/8/8 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.our_pieces_count == 3
    assert board_features.their_pieces_count == 3
    assert board_features.all_pieces_count == 6
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.our_pieces_count == 3
    assert board_features.their_pieces_count == 3
    assert board_features.all_pieces_count == 6


def test_connectivity():
    fen = "4qkr1/5b2/8/4Q3/2N5/3P1B2/1BP1R3/2K5 w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connectivity == 13
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.connectivity == 8

    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connectivity == 18
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.connectivity == 9


def test_material_vector_count():
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.material_vector_count == [8, 2, 2, 2, 1, 1]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.material_vector_count == [8, 2, 2, 2, 1, 1]

    fen = "4qkr1/5b2/8/4Q3/2N5/3P1B2/1BP1R3/2K5 w - - 0 19"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.material_vector_count == [2, 1, 2, 1, 1, 1]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.material_vector_count == [0, 0, 1, 1, 1, 1]

    fen = "qqqqqkr1/5bpp/8/4Q3/2N5/1P1P1B2/1BP1R3/2K1R2R b - - 0 22"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.material_vector_count == [3, 1, 2, 3, 1, 1]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.material_vector_count == [2, 0, 1, 1, 5, 1]


def test_connected_rooks():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_rooks
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_rooks

    fen = "r4rk1/2R4R/3P2B1/2Pb4/5P2/8/6PP/6K1 b - - 1 31"

    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connected_rooks
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.connected_rooks

    fen = "r4rk1/7R/2RP2B1/2Pb4/5P2/8/6PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_rooks
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.connected_rooks

    fen = "5rk1/5r1R/2RP2B1/2Pb4/5P2/8/6PP/6K1 b - - 1 31"

    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_rooks
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.connected_rooks

    fen = "5rk1/8/2RP2B1/2Pb4/5P2/8/6PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_rooks
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_rooks

    fen = "5rkr/2R5/3P2B1/2Pb4/5P2/8/2R3PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_rooks
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_rooks


def test_connected_knights():
    fen = "2n2rkr/2R5/3P2B1/1NPb4/4NP2/2N5/2R3PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_knights

    fen = "2n2rkr/2R5/3P2B1/1NPb4/4NP2/8/2R3PP/1N4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_knights

    fen = "2n2rkr/2R5/3P2B1/1NPb4/5P2/2N5/2R2NPP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_knights

    fen = "2n2rkr/2R5/3P2B1/1NPb4/5P2/2N5/2R3PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_knights

    fen = "2n2rkr/N1R5/3P2B1/2Pb4/5P2/2N5/2R3PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_knights

    fen = "6n1/N3n3/R1NPB3/2Pb4/R4P1k/1r6/6PP/1r4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.connected_knights

    fen = "8/8/R2PB3/2Pb4/R4P1k/1r6/6PP/1r4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.connected_knights
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.connected_knights


def test_bishop_pair():
    fen = "8/4B3/R2PB3/2Pb4/R4P1k/1r6/6PP/1r4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishop_pair
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.bishop_pair

    fen = "8/3BB3/R2P4/2P5/R1b2P1k/1rbb4/6PP/1r4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishop_pair
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishop_pair

    fen = "7R/8/R2P4/2P5/5P1k/1r6/6PP/1r4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert not board_features.bishop_pair
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.bishop_pair

    fen = "7R/2BB4/R2P4/2P5/5P1k/1r6/6PP/1r4K1 b - - 1 31"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishop_pair
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert not board_features.bishop_pair

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishop_pair
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishop_pair


def test_bishops_mobility():
    fen = "rnb1kbnr/pp1pppp1/8/5p2/P4P2/8/PP2PPP1/2R1KBNR b Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == [0]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [0, 0]

    fen = "rnb1kbnr/pp1pppp1/8/5p2/P4P2/6P1/PP2PP2/2R1KBNR b Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == [2]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [0, 0]

    fen = "rnb1kbnr/pp2pp2/3p2p1/5p2/P4P2/6P1/PP2PP2/2R1KBNR b Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == [2]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [2, 2]

    fen = "rn2kbnr/pp2pp2/3p2p1/5p2/P4P2/6P1/PP2PP2/2R1K1NR w Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == []

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [2]

    fen = "rn2k1nr/pp2pp2/3p2p1/5p2/Pb3P2/6P1/PP2PP2/2R1K1NR w Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == []

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [6]

    fen = "rn2k1nr/pp2pp2/3p2p1/5p2/Pb3P2/5BP1/PP2PP2/2R1K1NR w Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == [7]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [6]

    fen = "rn2k1nr/pp2pp2/3p2p1/5p2/P4P2/6P1/PP2PP2/2R1K1NR w Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == []

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == []

    fen = "5rk1/r5pp/1b1qp2n/PP1p4/3P4/3K4/2BN1PPP/2RQN3 w - - 0 30"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_mobility == [3]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_mobility == [5]


def test_knights_mobility():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_mobility == [2, 2]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_mobility == [2, 2]

    fen = "r1bqkb1r/1ppp1ppp/p1n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1R1K w Qkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_mobility == [2, 6]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_mobility == [5, 6]

    fen = "2rqkb1r/1p1p1ppp/p2n4/1p3p2/2p1b3/5N2/PPPP1PPP/RNBQ1R1K w Qk - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_mobility == [2, 6]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_mobility == [0]

    fen = "2rqkb1r/1p1p1ppp/p7/1p3p2/2p1b3/8/PPPP1PPP/R1BQ1R1K w Qk - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_mobility == []
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_mobility == []


def test_rooks_mobility():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.rooks_mobility == [0, 0]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.rooks_mobility == [0, 0]

    fen = "2rqkb1r/1p1p1ppp/p7/1p3p2/2p1b3/8/PPPP1PPP/R1BQ1R1K w Qk - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.rooks_mobility == [1, 2]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.rooks_mobility == [1, 5]

    fen = "2rqkb1r/1p1p1pp1/p5p1/1p3p2/2p1b3/1P4P1/1PPP2PP/R1BQ1R1K b Qk - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.rooks_mobility == [6, 6]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.rooks_mobility == [5, 7]

    fen = "2rqk2r/1p1p1pp1/p5p1/bp3p2/2p1b3/1P3PP1/1PPP2P1/R1BQ1R1K w Qk - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.rooks_mobility == [3, 5]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.rooks_mobility == [5, 9]

    fen = "5rk1/r5pp/1b1qp2n/PP1p4/3P4/8/2KN1PPP/2RQN3 w - - 0 30"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.rooks_mobility == [2]
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.rooks_mobility == [8, 11]


def test_knights_centrality():
    fen = "r2qk1nr/ppp2ppp/8/3nN3/8/6PP/PPP1PP2/RN1QK2R w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_centrality == [0, 3]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_centrality == [0, 3]

    fen = "r2qk1nr/ppp2ppp/8/2n5/4N3/6PP/PPP1PP2/RN1QK2R w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_centrality == [0, 3]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_centrality == [1, 3]

    fen = "r2qk2r/ppp2ppp/8/2nn4/3NN3/6PP/PPP1PP2/R2QK2R w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_centrality == [0, 0]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_centrality == [0, 1]

    fen = "r2qk2r/ppp2ppp/8/2n2n2/3NN3/6PP/PPP1PP2/R2QK2R b KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_centrality == [0, 0]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_centrality == [1, 1]

    fen = "r2qk2r/ppp2ppp/8/8/3N4/6PP/PPP1PP2/R2QK2R b KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_centrality == [0]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_centrality == []

    fen = "r2qk2r/ppp2ppp/8/8/8/6PP/PPP1PP2/R2QK2R b KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.knights_centrality == []

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.knights_centrality == []


def test_bishop_centrality():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_centrality == [3, 3]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_centrality == [3, 3]

    fen = "rnbqkbnr/ppp2ppp/8/3pB3/3P4/8/PPP1PPPP/RN1QKBNR w KQkq - 0 4"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_centrality == [0, 3]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_centrality == [3, 3]

    fen = "rnbqkbnr/ppp2ppp/8/3pB3/3P4/8/PPP1PPPP/RN1QK1NR w KQkq - 0 4"

    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_centrality == [0]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_centrality == [3, 3]

    fen = "rn1qkbnr/pp3ppp/8/3bB3/3p4/6PP/PPP1PP2/RN1QK1NR w KQkq - 0 10"

    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_centrality == [0]

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_centrality == [0, 3]

    fen = "rn1qk1nr/pp3ppp/8/8/3p4/6PP/PPP1PP2/RN1QK1NR w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.bishops_centrality == []

    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.bishops_centrality == []


def test_queen_centrality():
    fen = "rnb1kbnr/pppppppp/8/8/P2q4/8/PP2PPPP/R3KBNR w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_centrality == [0]

    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_centrality == []

    fen = "rnb1kbnr/pppppppp/7Q/8/P2q4/8/PP2PPPP/R3KBNR w KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_centrality == [0]

    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_centrality == [3]

    fen = "rnb1kbnr/pppppppp/7Q/3Q4/P2q4/8/PP2PPPP/R3KBNR b KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_centrality == [0]

    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_centrality == [0, 3]

    fen = "rnb1kbnr/pppppppp/8/8/P7/8/PP2PPPP/R3KBNR b KQkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.queens_centrality == []

    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.queens_centrality == []


def test_open_files_rooks_count():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.open_files_rooks_count == 0
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.open_files_rooks_count == 0

    fen = "rnb1kbnr/pp1pppp1/8/5p2/P4P2/8/PP2PPP1/2R1KBNR b Kkq - 0 10"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.open_files_rooks_count == 2
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.open_files_rooks_count == 1


def test_our_legal_moves_count():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.legal_moves_count == 20
    board_features = BoardFeatures(board, color=chess.BLACK)
    assert board_features.legal_moves_count == 20

    fen = "rnb1kbnr/pppppppp/8/8/Pq6/8/PP2PPPP/R3KBNR w KQkq - 0 1"
    board = chess.Board(fen)
    board_features = BoardFeatures(board, color=chess.WHITE)
    assert board_features.legal_moves_count == 1
