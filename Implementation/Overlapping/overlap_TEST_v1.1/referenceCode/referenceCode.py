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

# Specify the rotation settings
# ts = ax1.transData
# coords = [1,0]
# tr = matplotlib.transforms.Affine2D().rotate_deg_around(coords[0],coords[1], 10)
# t = tr + ts

#rec0 = matplotlib.patches.Rectangle((-1,-0.5),1,0.5,linewidth=1,edgecolor='r',facecolor='none')
#ax1.add_patch(rec0)
#Rotated rectangle patch
#rect1 = matplotlib.patches.Rectangle((0,-1),2,2,linewidth=1,edgecolor='b',facecolor='none',transform=t)
#ax1.add_patch(rect1)

#plt.text(-0.95, -0.4, literals[0], fontsize = 16)
# drawLiteral("ABCD", [0,0], 60, plt)
# drawRectangle("ABCD", [0,0], 60, plt)
# drawLiteral("AEFGH", [0,0], 120, plt)
# drawRectangle("AEFGH", [0,0], 120, plt)

# literalsNum = len(literalsList)
# rotateRate = 360 / literalsNum
# i = 0
# for center in centersList:
#     rotateAngle = rotateRate * i
#     drawLiteral(literalsList[i], center, rotateAngle, plt)
#     drawRectangle(literalsList[i], center, rotateAngle, plt)
#     i = i + 1