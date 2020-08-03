# Classic Tetris

This game is made with python module pygame with the help from tutorials made by Tech With Tim. I used his code for building blocks, improved on it, fixed bugs, and added few features that I will talk about more in further application description.

![tetris game](https://user-images.githubusercontent.com/59142427/89187724-f24dfb00-d59d-11ea-9384-2f8e3d6dfeb9.gif)

## Features I added to original

* Added classical movement control possibility for players
    * On keyboard space-key press, piece speeds up towards bottom of the field
    * Previously when player was moving piece left and right on playing field, it was required to continuosly press left arrow key to move piece towards left playing field border and same goes for movement towards right, with each keyboard key press piece would move only one square in desired direction. Now you can just press down left or right arrow key and piece is moving with continuous speed towards left or right border
* Added background music, sound effect for clearing rows and game over melody
* Added function for play testing (It will be shown and explained how it's been used, in further text below) 
* Changed the looks of the original table, color scheme, next piece section
* Added bonus points for clearing 2,3 and 4 rows simultaneously
* Added score rules label and bonus points label
* Fixed a bug where continuous button pressed before new piece started falling down the field could lose you the game because piece would end out of legal playing bounds
* Fixed a bug for clearing rows (more details in further description below)

## Clearing rows function Bug

### Bug description 
Bug I came across in the original code (when playing a game) shown in gif below. Clearing rows is not a problem but shifting everything down to its place is where the bug appeared.

![original bad function](https://user-images.githubusercontent.com/59142427/89187835-1578aa80-d59e-11ea-9473-65a8b5052ca0.gif)

Although this is an edge case and it doesn't appear often in actual game when beginner is playing, when it happens it ruins the whole tetris experience, and guys like [pro tetris players](https://www.youtube.com/watch?v=L_UPHsGR6fM) wouldn't be happy about it, so I decide to fix it.
 
 ### Solution to bug

 It was time consuming to check how changes in code made the difference in actual game (especially for function clear rows edge cases), because it was necessary to first create a board that is edge case (four complete lines ready to be cleared, with only a gap on second or third line), like shown in example above.

 So I made a function which secures that position at the beginning of the game is optimal for testing and also made changes in code so that long piece (I piece) is first to fall. After doing that, it was tremendously easier to test even the slightest changes in code and see the results immediately.

 To implement testing functions just change in main function variable locked positions from "{}" (empty dictionary) to "make_locked()" and if you want that first piece that falls is "I piece" change current_piece variable in main function to current_piece = Piece(9,7,shapes[2])

 This is original code with the bug:

```python
def clear_rows(grid, locked,surface):
    inc = 0
    for i in range(len(grid) - 1, -1,-1):  
        row = grid[i]
        if (0, 0, 0) not in row:  
            inc += 1
            index_num = i  
            for j in range(len(row)):
                try:
                    del locked[(j, i)]  
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < index_num:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
```

 It has that problem where after it cleared the rows it shifted all the lines towards bottom with the same increment, so it was necessary to modify that, and make unique down shifting pattern for all four cases, and in code below you can see how I did it and solve the problem:

```python
 def clear_rows(grid, locked, surface):
    deleted_rows = []
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row: 
            inc += 1
            for j in range(len(row)):
                del locked[(j, i)]
            deleted_rows.append(i)

    if len(deleted_rows) == 1 or len(deleted_rows) == 4:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < deleted_rows[0]:
                newKey = (x, y + len(deleted_rows))
                locked[newKey] = locked.pop(key)
    elif len(deleted_rows) == 2:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < deleted_rows[0] and y > deleted_rows[1]:
                newKey = (x, y + 1)
                locked[newKey] = locked.pop(key)
            elif y < deleted_rows[1]:
                newKey = (x, y + 2)
                locked[newKey] = locked.pop(key)
    elif len(deleted_rows) == 3:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < deleted_rows[0] and y > deleted_rows[1]:
                newKey = (x, y + 1)
                locked[newKey] = locked.pop(key)
            elif y < deleted_rows[1] and y > deleted_rows[2]:
                newKey = (x, y + 2)
                locked[newKey] = locked.pop(key)
            elif y < deleted_rows[2]:
                newKey = (x, y + 3)
                locked[newKey] = locked.pop(key)
```

 After these modifications everything worked how it should, and that looks like this.

 ![good func](https://user-images.githubusercontent.com/59142427/89187904-3214e280-d59e-11ea-86db-59b4d6a18bcc.gif)
