//Tic Tac Toe - Two Player CLI Game in Rust
use std::io;

fn create_empty_board() -> [[char; 3]; 3] {
    [['0'; 3]; 3]
}

fn present(row: [char; 3]) -> [char; 3] {
    let mut presentation = ['.'; 3];
    for i in 0..3 {
        if row[i] == '1' || row[i] == '2' {
            presentation[i] = row[i];
        } 
    }
    presentation
}

fn display_board(board: [[char; 3]; 3]) {
    println!("    0   1   2  ");
    println!("  -------------");
    for i in 0..3 {
        let row = board[i];
        let p = present(row);
        println!("{} | {} | {} | {} |", i, p[0], p[1], p[2]);
        println!("  -------------");
    }
}

fn is_valid_move(board: [[char; 3]; 3], row: usize, col: usize) -> bool {
    if row <= 2  {
        if col <= 2  {
            if board[row][col] == '0' {
                return true;
            }
        }
    }
    false
}

fn make_move(mut board: [[char; 3]; 3], row: usize, col: usize, player: char) -> [[char; 3]; 3] {
    if player == '1'{
        board[row][col] = '1';
    } else if player == '2'{
        board[row][col] = '2';
    }
    board
}

fn check_winner(board: [[char; 3]; 3]) -> Option<char> {
    // diagonal
    if board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != '0' {
        return Some(board[0][0]);
    }
    if board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != '0' {
        return Some(board[0][2]);
    }
    // horizontal and vertical
    for i in 0..3 {
        if board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != '0' {
            return Some(board[i][0]);
        }
        if board[0][i] == board[1][i] && board[1][i] == board[2][i] && board[0][i] != '0' {
            return Some(board[0][i]);
        }
    }
    None
}

fn is_board_full(board: [[char; 3]; 3]) -> bool {
    for i in 0..3 {
        for j in 0..3 {
            if board[i][j] == '0' {
                return false;
            }
        }
    }
    true
}

fn get_player_move(player: char) -> (usize, usize) {
    println!("Player {} input your next move in this format:\n row,col (0th index-ed)\n", player);
    let mut guess = String::new();
    io::stdin().read_line(&mut guess).expect("failed to read line");
    let parts: Vec<&str> = guess.trim().split(',').collect();
    let row: usize = parts[0].trim().parse().expect("invalid row");
    let col: usize = parts[1].trim().parse().expect("invalid col");
    (row, col)
}

fn play_game() {
    let mut player = '1';
    let mut board = create_empty_board();
    display_board(board);
    while !is_board_full(board) {
        let row;
        let col;
        loop {
            let (r, c) = get_player_move(player);
            if is_valid_move(board, r, c) {
                row = r;
                col = c;
                break;
            }
            println!("Input move invalid. Check the following and try again:\n 1) row and col are within bounds (0-2)\n 2) The target square is empty");
        }
        board = make_move(board, row, col, player);
        display_board(board);
        if let Some(winner) = check_winner(board) {
            println!("Winner: Player {}", winner);
            break;
        } else {
            if player == '1' {
                player = '2';
            } else if player == '2' {
                player = '1';
            }
        }
    }
    if check_winner(board).is_none() {
        println!("Game Ended: It's a cat's game!\n https://english.stackexchange.com/questions/155621/why-is-a-tie-in-tic-tac-toe-called-a-cats-game");
    }
}

fn main() {
    play_game();
}
