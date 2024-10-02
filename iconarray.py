import numpy as np

def create_grid(n):
    if n < 0 or n > 100:
        print("Please enter a value for n between 0 and 100.")
        return
    
    # Create an array with n smileys and (100-n) nauseated faces
    emojis = ['<div>🤢</div>'] * n + ['<div>😊</div>'] * (100 - n)
    
    # Shuffle the array
    np.random.shuffle(emojis)
    
    # Reshape the array into a 10x10 grid
    grid = np.array(emojis).reshape(10, 10)
    
    # Print the grid
    print('<div class="icon-array">')
    for row in grid:
        print('<!-- row -->')
        print(''.join(row))
    print('</div>')
    
# Input value for n
n = int(input("Enter a value for n (0 to 100): "))
create_grid(n)