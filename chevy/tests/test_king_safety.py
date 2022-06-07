import chess

from chevy.features import KingSafety


def test_king_at_check():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert not king_safety.checked
    king_safety = KingSafety(board, color=chess.BLACK)
    assert not king_safety.checked

    # https://lichess.org/analysis/2r3k1/7R/6PK/6P1/2Q5/8/8/8_b_-_-_6_73
    fen = "2r3k1/7R/6PK/6P1/2Q5/8/8/8 b - - 6 73"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert not king_safety.checked
    king_safety = KingSafety(chess.Board(fen), color=chess.BLACK)
    assert king_safety.checked

    # https://lichess.org/editor/k1r5/4K2R/6P1/6P1/8/5B2/8/8_b_-_-_6_73
    fen = "k1r5/4K2R/6P1/6P1/8/5B2/8/8 b - - 6 73"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert not king_safety.checked
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.checked

    # https://lichess.org/editor/r1b2r2/p2pp2p/5k2/q1p1N3/2pnPPQ1/2N5/PPPP2PP/R1B2RK1_w_-_-_2_14
    fen = "r1b2r2/p2pp2p/5k2/q1p1N3/2pnPPQ1/2N5/PPPP2PP/R1B2RK1 w - - 2 14"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert not king_safety.checked
    king_safety = KingSafety(board, color=chess.BLACK)
    assert not king_safety.checked

    fen = "r1b2r2/p2pp2p/5k2/q1p1N1Q1/2pnPP2/2N5/PPPP2PP/R1B2RK1 b - - 3 14"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert not king_safety.checked
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.checked


def test_castling_rights():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.castling_rights
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.castling_rights

    # https://lichess.org/editor/k1r5/4K2R/6P1/6P1/8/5B2/8/8_b_-_-_6_73
    fen = "k1r5/4K2R/6P1/6P1/8/5B2/8/8 b - - 6 73"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert not king_safety.castling_rights
    king_safety = KingSafety(board, color=chess.BLACK)
    assert not king_safety.castling_rights


def test_king_attackers_looking_at_ring_1():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert sum(king_safety.king_attackers_looking_at_ring_1) == 0

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_looking_at_ring_1) == 0

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q1bp3/4P3/2K5/P4rPP/RNBQ1BNR_w_q_-_0_19
    fen = "r3kbn1/pppp1ppp/3n4/1q1bp3/4P3/2K5/P4rPP/RNBQ1BNR w q - 0 19"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_looking_at_ring_1 == [1, 1, 1, 1, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_looking_at_ring_1) == 0

    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"

    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_looking_at_ring_1 == [1, 1, 2, 0, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_looking_at_ring_1) == 0


def test_king_attackers_at_ring_1():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert sum(king_safety.king_attackers_at_ring_1) == 0

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_at_ring_1) == 0

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/2K5/P4rPP/RNBQ1BNR_w_q_-_0_19
    fen = "r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/2K5/P4rPP/RNBQ1BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_at_ring_1 == [0, 0, 1, 0, 0, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_at_ring_1) == 0

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2brP3/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2brP3/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_at_ring_1 == [0, 0, 1, 1, 0, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_at_ring_1) == 0


def test_king_defenders_at_ring_1():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_at_ring_1 == [3, 0, 1, 0, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_at_ring_1 == [3, 0, 1, 0, 1, 0]

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR_w_q_-_0_19
    fen = "r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_at_ring_1 == [0, 0, 0, 0, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_at_ring_1 == [2, 0, 1, 0, 0, 0]

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_at_ring_1 == [0, 0, 0, 0, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_at_ring_1 == [2, 0, 0, 0, 0, 0]


def test_king_defenders_looking_at_ring_1():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_looking_at_ring_1 == [0, 2, 2, 0, 1, 1]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_looking_at_ring_1 == [0, 2, 2, 0, 1, 1]

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR_w_q_-_0_19
    fen = "r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_looking_at_ring_1 == [1, 1, 2, 0, 1, 1]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_looking_at_ring_1 == [0, 2, 2, 2, 1, 1]

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_looking_at_ring_1 == [1, 1, 2, 0, 1, 1]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_looking_at_ring_1 == [0, 2, 1, 1, 1, 1]


def test_king_attackers_looking_at_ring_2():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert sum(king_safety.king_attackers_looking_at_ring_2) == 0

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_looking_at_ring_2) == 0

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n3b/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_looking_at_ring_2 == [0, 1, 2, 1, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_attackers_looking_at_ring_2 == [0, 0, 0, 0, 0, 0]

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_looking_at_ring_2 == [0, 1, 1, 1, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_attackers_looking_at_ring_2 == [0, 0, 0, 0, 0, 0]


def test_king_attackers_at_ring_2():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert sum(king_safety.king_attackers_at_ring_2) == 0

    king_safety = KingSafety(board, color=chess.BLACK)
    assert sum(king_safety.king_attackers_at_ring_2) == 0

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n3b/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_at_ring_2 == [1, 0, 0, 0, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_attackers_at_ring_2 == [0, 0, 0, 0, 0, 0]

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_attackers_at_ring_2 == [1, 0, 1, 0, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_attackers_at_ring_2 == [0, 0, 0, 0, 0, 0]


def test_king_defenders_at_ring_2():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_at_ring_2 == [2, 1, 1, 0, 0, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_at_ring_2 == [2, 1, 1, 0, 0, 0]

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n3b/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_at_ring_2 == [2, 1, 1, 1, 0, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_at_ring_2 == [2, 2, 0, 0, 0, 0]

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_at_ring_2 == [2, 1, 1, 1, 0, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_at_ring_2 == [2, 2, 0, 0, 0, 0]


def test_king_defenders_looking_at_ring_2():
    # starting position
    # [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_looking_at_ring_2 == [7, 2, 1, 1, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_looking_at_ring_2 == [7, 2, 1, 1, 1, 0]

    # https://lichess.org/editor/r3kbn1/pppp1ppp/3n4/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n3b/1q2p3/2b1P3/1QK5/P4rPP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_looking_at_ring_2 == [1, 2, 2, 1, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_looking_at_ring_2 == [6, 2, 2, 2, 1, 0]

    # https://lichess.org/editor/r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR_w_q_-_0_19
    fen = "r3k1n1/pppp1ppp/3n4/bq2p3/2b1P1r1/1QK5/P5PP/RNB2BNR w q - 0 19"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_defenders_looking_at_ring_2 == [1, 2, 2, 1, 1, 0]

    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_defenders_looking_at_ring_2 == [6, 2, 2, 2, 1, 0]


def test_king_centrality():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_centrality == 3
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_centrality == 3

    # https://lichess.org/editor/2r5/7R/4K1P1/6P1/3k4/8/8/8_b_-_-_6_73
    fen = "2r5/7R/4K1P1/6P1/3k4/8/8/8 b - - 6 73"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_centrality == 1
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_centrality == 0

    # https://lichess.org/editor/7K/2r4R/6P1/6P1/8/8/8/k7_w_-_-_6_73
    fen = "7K/2r4R/6P1/6P1/8/8/8/k7 w - - 6 73"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_centrality == 3
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_centrality == 3

    # https://lichess.org/editor/8/2r4R/6P1/1k4P1/8/7K/8/8_w_-_-_6_73
    fen = "8/2r4R/6P1/1k4P1/8/7K/8/8 w - - 6 73"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_centrality == 3
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_centrality == 2


def test_king_mobility():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 0
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 0

    # https://lichess.org/editor/2r3k1/7R/6PK/6P1/8/8/8/8_b_-_-_6_73
    fen = "2r3k1/7R/6PK/6P1/8/8/8/8 b - - 6 73"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 1
    king_safety = KingSafety(chess.Board(fen), color=chess.BLACK)
    assert king_safety.king_mobility == 1

    # https://lichess.org/editor/k1r5/4K2R/6P1/6P1/8/8/8/8_b_-_-_6_73
    fen = "k1r5/4K2R/6P1/6P1/8/8/8/8 b - - 6 73"
    board = chess.Board(fen)

    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 5
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 3

    # https://lichess.org/editor/r1b2r2/p2pp2p/5k2/q1p1N3/2pnPPQ1/2N5/PPPP2PP/R1B2RK1_w_-_-_2_14
    fen = "r1b2r2/p2pp2p/5k2/q1p1N3/2pnPPQ1/2N5/PPPP2PP/R1B2RK1 w - - 2 14"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 2
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 0

    # https://lichess.org/editor/r4rk1/2R4R/3P2Bp/2Pb1p2/p4Pp1/8/6PP/6K1_b_-_-_1_31
    fen = "r4rk1/2R4R/3P2Bp/2Pb1p2/p4Pp1/8/6PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 3
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 0

    # https://lichess.org/editor/r7/R7/8/8/8/8/2k1K3/8_b_-_-_1_31
    fen = "r7/R7/8/8/8/8/2k1K3/8 b - - 1 31"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 5
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 5

    # https://lichess.org/editor/r7/R7/8/8/2k2K2/8/8/8_b_-_-_1_31
    fen = "r7/R7/8/8/2k2K2/8/8/8 b - - 1 31"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 8
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 8

    # https://lichess.org/editor/1kr5/R2K4/R7/4q3/8/8/8/8_b_-_-_1_31
    fen = "1kr5/R2K4/R7/4q3/8/8/8/8 b - - 1 31"
    board = chess.Board(fen)
    king_safety = KingSafety(board, color=chess.WHITE)
    assert king_safety.king_mobility == 0
    king_safety = KingSafety(board, color=chess.BLACK)
    assert king_safety.king_mobility == 0
