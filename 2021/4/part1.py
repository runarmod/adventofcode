def checkBoard(board, nums):
    # Check rows
    for row in board:
        for num in row:
            if num not in nums:
                break
        else:
            return True
    # Check columns
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[j][i] not in nums:
                break
        else:
            return True

def calculateBoard(board, nums):
    return sum(1 for row in board for num in row if num not in nums) * nums[-1]


def main():
    boards = open("input.txt").read().rstrip().split("\n\n")
    picks = list(map(int, boards.pop(0).split(",")))

    for i in range(len(boards)):
        boards[i] = boards[i].split("\n")
        for j in range(len(boards[i])):
            boards[i][j] = list(map(int, filter(None, boards[i][j].split(" "))))
    
    
    for i in range(len(picks)):
        if i < 5: continue
        for board in boards:
            if checkBoard(board, picks[:i]):
                print("Answer:", calculateBoard(board, picks[:i]))
                print("Winner:", picks[:i], board)
                return


if __name__ == "__main__":
    main()