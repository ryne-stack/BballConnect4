import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { RotateCcw, Undo2, Trophy, Edit3, CircleDashed } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const ROWS = 5;
const COLS = 5;

const createEmptyBoard = () =>
  Array.from({ length: ROWS }, () => Array(COLS).fill(null));

const getDropRow = (board, col) => {
  for (let row = ROWS - 1; row >= 0; row--) {
    if (!board[row][col]) return row;
  }
  return -1;
};

const checkWinner = (board) => {
  const directions = [
    [0, 1],
    [1, 0],
    [1, 1],
    [1, -1],
  ];

  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const player = board[row][col];
      if (!player) continue;

      for (const [dr, dc] of directions) {
        const cells = [[row, col]];

        for (let step = 1; step < 4; step++) {
          const r = row + dr * step;
          const c = col + dc * step;

          if (r < 0 || r >= ROWS || c < 0 || c >= COLS) break;
          if (board[r][c] !== player) break;

          cells.push([r, c]);
        }

        if (cells.length === 4) {
          return { winner: player, cells };
        }
      }
    }
  }

  const isDraw = board.every((row) => row.every(Boolean));
  return isDraw ? { winner: "draw", cells: [] } : null;
};

const isWinningCell = (winningCells, row, col) =>
  winningCells.some(([r, c]) => r === row && c === col);

function BasketballToken({ variant }) {
  const fillColor = variant === "yellow" ? "#2563eb" : "#f85d12";

  return (
    <div className="h-9 w-9 md:h-12 md:w-12">
      <svg viewBox="0 0 100 100" className="h-full w-full" aria-hidden="true">
        <circle cx="50" cy="50" r="46" fill={fillColor} stroke="#000" strokeWidth="5" />
        <path d="M50 4 V96" stroke="#000" strokeWidth="5" strokeLinecap="round" />
        <path d="M4 50 H96" stroke="#000" strokeWidth="5" strokeLinecap="round" />
        <path d="M20 28 C35 18 65 18 80 28" fill="none" stroke="#000" strokeWidth="5" strokeLinecap="round" />
        <path d="M20 72 C35 82 65 82 80 72" fill="none" stroke="#000" strokeWidth="5" strokeLinecap="round" />
      </svg>
    </div>
  );
}

function HoopIcon() {
  return (
    <div className="flex flex-col items-center justify-end h-20">
      <svg viewBox="0 0 120 100" className="w-16 md:w-20" aria-hidden="true">
        {/* backboard */}
        <rect x="30" y="5" width="60" height="40" rx="4" fill="#ffffff" stroke="#cbd5e1" strokeWidth="3" />

        {/* backboard square */}
        <rect x="48" y="18" width="24" height="18" fill="none" stroke="#ef4444" strokeWidth="3" />

        {/* rim */}
        <ellipse cx="60" cy="48" rx="22" ry="6" fill="#ea580c" stroke="#9a3412" strokeWidth="2" />

        {/* net */}
        <g stroke="#e5e7eb" strokeWidth="2">
          <line x1="42" y1="48" x2="50" y2="72" />
          <line x1="50" y1="48" x2="54" y2="74" />
          <line x1="60" y1="48" x2="60" y2="76" />
          <line x1="70" y1="48" x2="66" y2="74" />
          <line x1="78" y1="48" x2="70" y2="72" />

          <line x1="48" y1="60" x2="72" y2="60" />
          <line x1="52" y1="68" x2="68" y2="68" />
        </g>
      </svg>
    </div>
  );
}

export default function ConnectFourBasketballTracker() {
  
  const [board, setBoard] = useState(createEmptyBoard());
  const [currentPlayer, setCurrentPlayer] = useState("red");
  const [history, setHistory] = useState([]);
  const [teamOne, setTeamOne] = useState("Orange Team");
  const [teamTwo, setTeamTwo] = useState("Blue Team");
  const [editingNames, setEditingNames] = useState(false);
  const [lastAction, setLastAction] = useState(null);

  const result = useMemo(() => checkWinner(board), [board]);
  const winningCells = result?.cells ?? [];

  const playerConfig = {
    red: {
      label: teamOne,
      soft: "bg-orange-100",
      ring: "ring-orange-300",
    },
    yellow: {
      label: teamTwo,
      soft: "bg-amber-100",
      ring: "ring-amber-300",
    },
  };

  const handleDrop = (col) => {
    
    if (result?.winner) return;

    const row = getDropRow(board, col);
    if (row === -1) return;

    const nextBoard = board.map((r) => [...r]);
    nextBoard[row][col] = currentPlayer;

    setHistory((prev) => [...prev, { board, currentPlayer, lastAction }]);
    setBoard(nextBoard);
    setLastAction({ type: "make", player: currentPlayer, column: col + 1 });
    setCurrentPlayer((prev) => (prev === "red" ? "yellow" : "red"));
  };

  const handleMiss = () => {
    if (result?.winner) return;
    setHistory((prev) => [...prev, { board, currentPlayer, lastAction }]);
    setLastAction({ type: "miss", player: currentPlayer });
    setCurrentPlayer((prev) => (prev === "red" ? "yellow" : "red"));
  };

  const handleUndo = () => {
    if (!history.length) return;
    const previous = history[history.length - 1];
    setBoard(previous.board);
    setCurrentPlayer(previous.currentPlayer);
    setLastAction(previous.lastAction ?? null);
    setHistory((prev) => prev.slice(0, -1));
  };

  const handleReset = () => {
    setBoard(createEmptyBoard());
    setCurrentPlayer("red");
    setHistory([]);
    setLastAction(null);
  };

  const handleCellClick = (row, col) => {
    const value = board[row][col];
    if (!value || result?.winner) return;

    const nextBoard = board.map((r) => [...r]);
    nextBoard[row][col] = null;
    setHistory((prev) => [...prev, { board, currentPlayer, lastAction }]);
    setBoard(nextBoard);
  };

  const statusText = result?.winner === "draw"
    ? "It is a draw."
    : result?.winner
    ? `${playerConfig[result.winner].label} wins.`
    : `${playerConfig[currentPlayer].label} is up.`;

  const lastActionText = !lastAction
    ? "No shots recorded yet."
    : lastAction.type === "miss"
    ? `${playerConfig[lastAction.player].label} missed. Possession switched.`
    : `${playerConfig[lastAction.player].label} made it and dropped into column ${lastAction.column}.`;

  return (
    <>
      
      <div className="min-h-screen bg-gradient-to-b from-slate-100 to-orange-50 p-6">
      <div className="mx-auto max-w-6xl space-y-6">
        <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <Card className="rounded-3xl border-0 shadow-xl">
            <CardContent className="p-6 md:p-8">
              <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <h1 className="text-3xl font-bold tracking-tight text-slate-900">
                    Connect Four Basketball
                  </h1>
                  <p className="mt-2 text-sm text-slate-600">
                    Click a hoop above any column to drop a basketball and track your live team challenge.
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="outline"
                    className="rounded-2xl"
                    onClick={() => setEditingNames((prev) => !prev)}
                  >
                    <Edit3 className="mr-2 h-4 w-4" />
                    {editingNames ? "Done" : "Edit teams"}
                  </Button>
                  <Button
                    variant="outline"
                    className="rounded-2xl"
                    onClick={handleUndo}
                    disabled={!history.length}
                  >
                    <Undo2 className="mr-2 h-4 w-4" />
                    Undo
                  </Button>
                  <Button className="rounded-2xl bg-orange-600 hover:bg-orange-700" onClick={handleReset}>
                    <RotateCcw className="mr-2 h-4 w-4" />
                    Reset
                  </Button>
                </div>
              </div>

              <div className="mb-6 grid gap-4 md:grid-cols-2">
                <motion.div
                  layout
                  className={`rounded-3xl p-4 ring-2 ${
                    currentPlayer === "red" && !result?.winner
                      ? `${playerConfig.red.soft} ${playerConfig.red.ring}`
                      : "bg-white ring-slate-200"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <BasketballToken variant="red" />
                    <div>
                      <div className="text-sm text-slate-500">Orange Team</div>
                      <div className="text-lg font-semibold text-slate-900">{teamOne}</div>
                    </div>
                  </div>
                </motion.div>

                <motion.div
                  layout
                  className={`rounded-3xl p-4 ring-2 ${
                    currentPlayer === "yellow" && !result?.winner
                      ? `${playerConfig.yellow.soft} ${playerConfig.yellow.ring}`
                      : "bg-white ring-slate-200"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <BasketballToken variant="yellow" />
                    <div>
                      <div className="text-sm text-slate-500">Team 2</div>
                      <div className="text-lg font-semibold text-slate-900">{teamTwo}</div>
                    </div>
                  </div>
                </motion.div>
              </div>

              {editingNames && (
                <div className="mb-6 grid gap-3 rounded-3xl bg-slate-100 p-4 md:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-700">
                      Team 1 name
                    </label>
                    <Input value={teamOne} onChange={(e) => setTeamOne(e.target.value)} />
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-700">
                      Team 2 name
                    </label>
                    <Input value={teamTwo} onChange={(e) => setTeamTwo(e.target.value)} />
                  </div>
                </div>
              )}

              <div className="mb-6 rounded-3xl bg-slate-100 p-4">
                <div className="mb-3 flex items-center justify-end gap-3">
                  <div className="text-sm font-medium text-slate-700">Current turn: {playerConfig[currentPlayer].label}</div>
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  <Button
                    variant="outline"
                    className="h-12 rounded-2xl border-orange-300 bg-white text-slate-900 hover:bg-orange-50"
                    onClick={handleMiss}
                    disabled={currentPlayer !== "red" || !!result?.winner}
                  >
                    Orange Team Miss
                  </Button>
                  <Button
                    variant="outline"
                    className="h-12 rounded-2xl border-blue-300 bg-white text-slate-900 hover:bg-blue-50"
                    onClick={handleMiss}
                    disabled={currentPlayer !== "yellow" || !!result?.winner}
                  >
                    Blue Team Miss
                  </Button>
                </div>
              </div>

              <div className="overflow-x-auto">
                <div className="mx-auto w-fit rounded-[2rem] bg-gradient-to-b from-blue-500 to-blue-700 p-4 shadow-2xl md:p-5">
                  <div className="mb-2 grid gap-2 md:gap-3" style={{ gridTemplateColumns: `repeat(${COLS}, minmax(0, 1fr))` }}>
                    {Array.from({ length: COLS }).map((_, col) => {
                      const disabled = getDropRow(board, col) === -1 || !!result?.winner;
                      return (
                        <button
                          key={col}
                          onClick={() => handleDrop(col)}
                          disabled={disabled}
                          className="group flex flex-col items-center rounded-2xl p-1 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
                          title="Drop basketball"
                        >
                          <HoopIcon />
                          <span className="mt-1 text-xs font-semibold uppercase tracking-wide text-white/85">
                            Drop
                          </span>
                        </button>
                      );
                    })}
                  </div>

                  <div className="grid gap-2 md:gap-3" style={{ gridTemplateColumns: `repeat(${COLS}, minmax(0, 1fr))` }}>
                    {board.map((row, rowIndex) =>
                      row.map((cell, colIndex) => {
                        const winning = isWinningCell(winningCells, rowIndex, colIndex);
                        return (
                          <motion.button
                            key={`${rowIndex}-${colIndex}`}
                            whileTap={{ scale: 0.96 }}
                            onClick={() => handleCellClick(rowIndex, colIndex)}
                            className={`relative flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 shadow-inner md:h-18 md:w-18 ${
                              winning ? "ring-4 ring-emerald-300" : ""
                            }`}
                            title={cell ? "Click to remove this basketball" : "Empty slot"}
                          >
                            {cell && (
                              <motion.div initial={{ y: -20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
                                <BasketballToken variant={cell} />
                              </motion.div>
                            )}
                          </motion.button>
                        );
                      })
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="space-y-6">
            <Card className="rounded-3xl border-0 shadow-xl">
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  {result?.winner && result.winner !== "draw" ? (
                    <Trophy className="h-6 w-6 text-slate-900" />
                  ) : (
                    <CircleDashed className="h-6 w-6 text-slate-900" />
                  )}
                  <div>
                    <div className="text-sm text-slate-500">Game status</div>
                    <div className="text-xl font-bold text-slate-900">{statusText}</div>
                  </div>
                </div>

                <div className="mt-5 rounded-3xl bg-orange-50 p-4 text-sm text-slate-700">
                  Use this as a live scoreboard while teams shoot mini basketballs in real life.
                  Each successful shot can equal one basketball dropped into the digital board.
                </div>

                <div className="mt-4 rounded-3xl bg-slate-100 p-4 text-sm text-slate-700">
                  <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Last action</div>
                  {lastActionText}
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-0 shadow-xl">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900">How to use it</h2>
                <div className="mt-4 space-y-3 text-sm leading-6 text-slate-600">
                  <p>1. Rename the teams if needed.</p>
                  <p>2. Click the hoop above the chosen column after each made basket.</p>
                  <p>3. If the active team misses, click that team’s Miss button to pass the turn without dropping a ball.</p>
                  <p>4. First team to connect four wins.</p>
                  <p>5. Click any placed basketball to remove it if a mistake happens.</p>
                  <p>6. Use Undo or Reset anytime during the activity.</p>
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-3xl border-0 shadow-xl">
              <CardContent className="p-6">
                <h2 className="text-lg font-semibold text-slate-900">Facilitator note</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  This version uses a 5 column by 5 row board with basketball themed tokens and hoops
                  above each column so it feels closer to your live mini hoop team challenge.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>      </div>
    </>
  );
}

