import chess
from chevy.features import PawnStructure


def test_central_pawns():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.central_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.central_pawns == 0

    # https://lichess.org/analysis/rnbqkbnr/ppp2ppp/8/3pp3/2PPP3/8/PP3PPP/RNBQKBNR_w_KQkq_-_0_4
    fen = "rnbqkbnr/ppp2ppp/8/3pp3/2PPP3/8/PP3PPP/RNBQKBNR w KQkq - 0 4"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.central_pawns == 2

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.central_pawns == 2

    # https://lichess.org/editor/5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5_w_-_-_0_19
    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.central_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.central_pawns == 0

    # https://lichess.org/editor/5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1_w_-_-_0_19
    fen = "5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.central_pawns == 1

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.central_pawns == 0


def test_blocked_pawns():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.blocked_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.blocked_pawns == 0

    # https://lichess.org/editor/5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5_w_-_-_0_19
    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.blocked_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.blocked_pawns == 0

    # https://lichess.org/editor/5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1_w_-_-_0_19
    fen = "5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.blocked_pawns == 1

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.blocked_pawns == 1


def test_isolated_pawns():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.isolated_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.isolated_pawns == 0

    # https://lichess.org/editor/5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5_w_-_-_0_19
    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.isolated_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.isolated_pawns == 0

    # https://lichess.org/editor/5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1_w_-_-_0_19
    fen = "5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.isolated_pawns == 1

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.isolated_pawns == 1

    # https://lichess.org/editor/5kr1/3ppp2/PQ2q3/2BP3P/2P4p/p7/4P3/1R2K1B1_w_-_-_0_19
    fen = "5kr1/3ppp2/PQ2q3/2BP3P/2P4p/p7/4P3/1R2K1B1 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.isolated_pawns == 2

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.isolated_pawns == 2


def test_double_pawns():
    # starting position
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.double_pawns == 0

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.double_pawns == 0

    # https://lichess.org/editor/5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5_w_-_-_0_19
    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.double_pawns == 1

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.double_pawns == 0

    # https://lichess.org/editor/5kr1/5p2/1Q1Pqp1p/1PBP3p/p7/1P1P4/8/1R2K1B1_w_-_-_0_19
    fen = "5kr1/5p2/1Q1Pqp1p/1PBP3p/p7/1P1P4/8/1R2K1B1 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.double_pawns == 2

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.double_pawns == 2


def test_passed_pawns():
    # https://lichess.org/editor/5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5_w_-_-_0_19
    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.passed_pawns == 2

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.passed_pawns == 2

    # https://lichess.org/editor/5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1_w_-_-_0_19
    fen = "5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.passed_pawns == 2

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.passed_pawns == 1


def test_pawn_islands():
    # https://lichess.org/editor/5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5_w_-_-_0_19
    fen = "5kr1/4pppp/4q3/8/2P5/1BQP4/1BP1P3/1RK5 w - - 0 19"
    board = chess.Board(fen)

    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.pawn_islands == 1

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.pawn_islands == 1

    # https://lichess.org/analysis/rnbqkbnr/ppp2ppp/8/3pp3/2PPP3/8/PP3PPP/RNBQKBNR_w_KQkq_-_0_4
    fen = "rnbqkbnr/ppp2ppp/8/3pp3/2PPP3/8/PP3PPP/RNBQKBNR w KQkq - 0 4"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.pawn_islands == 3

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.pawn_islands == 3

    # https://lichess.org/editor/r4rk1/2R4R/3P2Bp/2Pb1p2/p4Pp1/8/6PP/6K1_b_-_-_1_31
    fen = "r4rk1/2R4R/3P2Bp/2Pb1p2/p4Pp1/8/6PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.pawn_islands == 3

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.pawn_islands == 3

    # https://lichess.org/editor/r4rk1/2R4R/3P2B1/2Pb4/5P2/8/6PP/6K1_b_-_-_1_31
    fen = "r4rk1/2R4R/3P2B1/2Pb4/5P2/8/6PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.pawn_islands == 3

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.pawn_islands == 0


def test_pawns_advancements():
    fen = "r4rk1/2R4R/3P2B1/2Pb4/5P2/8/6PP/6K1 b - - 1 31"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.pawns_advancements == [-1, -1, 4, 5, -1, 3, 1, 1]

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.pawns_advancements == [-1, -1, -1, -1, -1, -1, -1, -1]

    fen = "6k1/5pp1/Qp2p3/7q/8/P5PK/2Br3P/8 w - - 3 36"
    board = chess.Board(fen)
    pawn_structure = PawnStructure(board, color=chess.WHITE)
    assert pawn_structure.pawns_advancements == [2, -1, -1, -1, -1, -1, 2, 1]

    pawn_structure = PawnStructure(board, color=chess.BLACK)
    assert pawn_structure.pawns_advancements == [-1, 5, -1, -1, 5, 6, 6, -1]
