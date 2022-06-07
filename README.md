## Simple framework for hand-crafted chess position evaluation

### Installation

To install please run

```shell
pip install chevy
```

### Basic usage

King safety features

```python
import chess
from chevy.features import KingSafety

# https://lichess.org/analysis/2r3k1/7R/6PK/6P1/2Q5/8/8/8_b_-_-_6_73
fen = "2r3k1/7R/6PK/6P1/2Q5/8/8/8 b - - 6 73"
board = chess.Board(fen)

king_safety = KingSafety(board, color=chess.WHITE)
print(f"{king_safety.king_mobility=}")
print(f"{king_safety.castling_rights=}")
print(f"{king_safety.king_centrality=}")
print(f"{king_safety.checked=}")
print(f"{king_safety.king_attackers_looking_at_ring_1=}")
print(f"{king_safety.king_defenders_at_ring_1=}")
# + more

```

Pawn structure features

```python
import chess
from chevy.features import PawnStructure

# https://lichess.org/editor/5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1_w_-_-_0_19
fen = "5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1 w - - 0 19"
board = chess.Board(fen)
pawn_structure = PawnStructure(board, color=chess.WHITE)
print(f"{pawn_structure.passed_pawns=}")
print(f"{pawn_structure.isolated_pawns=}")
print(f"{pawn_structure.blocked_pawns=}")
print(f"{pawn_structure.central_pawns=}")
print(f"{pawn_structure.central_pawns=}")


```

Other common features

```python
import chess
from chevy.features import BoardFeatures

# https://lichess.org/editor/5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1_w_-_-_0_19
fen = "5kr1/4pp1p/1Q2q3/1PBP2p1/2P3P1/p7/4P3/1R2K1B1 w - - 0 19"
board = chess.Board(fen)
pawn_structure = BoardFeatures(board, color=chess.WHITE)
print(f"{pawn_structure.bishop_pair=}")
print(f"{pawn_structure.fianchetto_queen=}")
print(f"{pawn_structure.fianchetto_king=}")
print(f"{pawn_structure.queens_mobility=}")
print(f"{pawn_structure.open_files_rooks_count=}")
print(f"{pawn_structure.connected_rooks=}")
print(f"{pawn_structure.connectivity=}")
# + more 



```

To run tests:

```shell
pytest chevy/tests 
```
