import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mPatches

#define Matplotlib figure and axis
fig, ax = plt.subplots()

# ax.plot([0, 10],[0, 10]) #create simple line plot
ax.add_patch(mPatches.Rectangle((0, 0), 1.5, 0.5)) #add rectangle to plot

pac = mPatches.Arc([0, -2.5], 5, 5, angle=0, theta1=45, theta2=135)
ax.add_patch(pac)
ax.axis([-2, 2, -2, 2])

#display plot
plt.text(0, 0, 'Parabola $Y = x^2$', fontsize = 22)
plt.show()
#fig.canvas.draw()