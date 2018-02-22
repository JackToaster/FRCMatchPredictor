import matplotlib.pyplot as plt


def two_box_plot(blue, red):
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot([blue,red], patch_artist=True)

    #change fill color
    bp['boxes'][0].set(facecolor='#0000EE')
    bp['boxes'][1].set(facecolor='#EE0000')

    #set labels
    ax.set_xticklabels(['Blue Score','Red Score'])

    ax.grid(True)

    # Save the figure
    plt.show(fig)
