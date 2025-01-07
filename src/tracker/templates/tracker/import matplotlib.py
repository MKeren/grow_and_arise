import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Set up the axis limits
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Draw the main problem box
ax.add_patch(mpatches.Rectangle((4, 8), 2, 1, edgecolor='black', facecolor='lightcoral'))
plt.text(5, 8.5, "Challenges", ha='center', va='center', fontsize=10)

# Draw solution boxes
solutions = ["Unified Tools", "Personalized Support", "Community Engagement", "Progress Tracking"]
y_positions = [6.5, 5, 3.5, 2]
colors = ['lightblue', 'lightgreen', 'khaki', 'lightpink']

for i, (sol, y) in enumerate(zip(solutions, y_positions)):
    ax.add_patch(mpatches.Rectangle((1, y), 3, 1, edgecolor='black', facecolor=colors[i]))
    plt.text(2.5, y + 0.5, sol, ha='center', va='center', fontsize=9)
    # Add arrow from challenges to solutions
    ax.arrow(5, 8, -2.5, y - 7.5, head_width=0.3, head_length=0.3, fc='gray', ec='gray')

# Add final result box
ax.add_patch(mpatches.Rectangle((6, 4), 3, 1, edgecolor='black', facecolor='lightgray'))
plt.text(7.5, 4.5, "Personal Growth", ha='center', va='center', fontsize=10)

# Add arrows from solutions to result
for y in y_positions:
    ax.arrow(4, y + 0.5, 2, -0.5, head_width=0.3, head_length=0.3, fc='gray', ec='gray')

plt.title("Simplified Flowchart: How 'Grow and Arise' Addresses Challenges", fontsize=12)
plt.tight_layout()
plt.show()
