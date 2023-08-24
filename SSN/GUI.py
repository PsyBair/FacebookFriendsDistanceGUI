from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure
import tkinter as tk
import time
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans


class GUI(tk.Frame):
    # Initializes window, __master is the root; __maps is a dictionary of all road networks; __socials is a dictionary
    # of all social networks, also __socials['networkHere.plot'] for the plots; __currentMap keeps track of the current
    # road network displayed; __currentSocial keeps track of the current social network displayed; __currentSocialUsers
    # keeps track of the current social users being displayed; __currentKeywords is a list of keyword objects being
    # displayed; __currentKeywordRels is a list of keyword object relations that are being displayed
    def __init__(self, master=None):
        t = time.perf_counter()
        print("Initializing GUI...")
        super().__init__(master, width=900, height=500)
        self.__master = master
        self.__maps = {}
        self.__socials = {}
        self.__currentMap = None
        self.__currentSocial = None
        self.__currentSocialStr = None
        self.__currentSocialUsers = None
        self.__currentKeywords = []
        self.__currentKeywordRels = []
        self.__currentSummary = None
        self.pack()
        self.mainMenuWidgets()
        self.focus_set()
        print(f"Done initializing. Took {round((time.perf_counter() - t), 3)} seconds")

    # Adds a map __maps
    def defMap(self, pointer, name):
        self.__maps[name] = pointer
        print(f"Added map {name}.")

    # Adds a social network to __socials
    def defSoc(self, pointer, name, color):
        self.__socials[name] = pointer
        self.__socials[f"{name}.relations.plot"] = None
        print(f"Added social network {name}.")

    # Displays the main menu widgets
    def mainMenuWidgets(self):
        self.__title = tk.Label(self.master, text="Spatial-Social Networks Visualizer", font=("Arial Black", 25))
        self.__pick = tk.Label(self.master, text="Pick a real world network", font=("Arial", 15))
        self.__californiaButton = tk.Button(text="Display California", font=("Arial", 15), height=2,
                                            command=lambda: self.map('california'))
        self.__title.place(relx=0.5, rely=0.1, anchor='center')
        self.__pick.place(relx=0.5, rely=0.2, anchor='center')
        self.__californiaButton.place(relx=0.5, rely=0.4, anchor='n', width=210)

    # Displays the main menu
    def mainMenu(self):
        self.__currentMap = None
        self.clearWindow()
        self.mainMenuWidgets()

    # Clears the window
    def clearWindow(self):
        self.destroy()
        super().__init__(self.master, width=900, height=700)
        self.pack()

    # Plots the points on the maps
    def map(self, key):
        t = time.perf_counter()
        print("Mapping data...")
        mapNetwork = self.__maps[key]
        self.__currentMap = key
        self.clearWindow()
        fig = Figure(figsize=(4.3, 3.3))
        fig.suptitle("Social Network")
        fig2 = Figure(figsize=(4.3, 3.3))
        fig2.suptitle("Real-World Network")
        fig3 = Figure(figsize=(3.3, 2.3))
        fig3.suptitle("Summary")
        plot1 = fig.add_subplot(111)
        plot2 = fig2.add_subplot(111)
        plot3 = fig3.add_subplot(111)
        # plotting the graph
        plot1.plot(mapNetwork.getPlottableLats(), mapNetwork.getPlottableLongs(), lw=0.25, c='black', picker=True,
                   pickradius=1000, label="Roads")
        plot1.legend(prop={"size": 7})
        plot2.set(xlim=plot1.get_xlim(), ylim=plot1.get_ylim())
        plot3.plot(mapNetwork.getPlottableLats(), mapNetwork.getPlottableLongs(), lw=0.25, c='black')
        canvas1 = FigureCanvasTkAgg(fig, master=self.master)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.master)
        canvas3 = FigureCanvasTkAgg(fig3, master=self.master)
        canvas1.draw()
        canvas2.draw()
        canvas3.draw()
        toolbar1 = NavigationToolbar2Tk(canvas1, self.master)
        toolbar2 = NavigationToolbar2Tk(canvas2, self.master)
        toolbar1.update()
        toolbar2.update()
        backButton = tk.Button(text="Back", font=("Arial", 15), height=1, command=self.mainMenu)
        selectedSocNetwork = tk.StringVar(self.master)
        selectedSocNetwork.trace_add('write', lambda *args: self.showRelations(plot1, plot2, plot3, canvas1, canvas2,
                                                                               canvas3, selectedSocNetwork.get()))
        selectKeywordButton = tk.Button(text="Select Keywords", font=("Arial", 15), height=1,
                                        command=lambda: self.showKeywords(canvas1, canvas2, plot1, plot2))
        socNetworkPicker = tk.OptionMenu(self.master, selectedSocNetwork, "gowalla", "tweets", "weibo",
                                         "foursquare")
        socNetworkPicker.config(font=("Arial", 15), height=1)
        clusterLabel = tk.Label(self.master, text="Summary Nodes:", font=("Arial", 15))
        self.__clusterChooser = tk.Spinbox(master=self.master, from_=0, to=100, font=("Arial", 15),
                                           textvariable=tk.DoubleVar(value=10), command=lambda *args:
                                           self.showSummary(self.__clusterChooser.get(), canvas3, plot3))
        selectedUser = tk.Label(self.master, text="Selected User", font=("Arial", 15))
        idLabel = tk.Label(self.master, text="ID:", font=("Arial", 15))
        self.__idLabel = tk.Label(self.master, text="NONE", font=("Arial", 10), fg='red')
        latitudeLabel = tk.Label(self.master, text="Lat:", font=("Arial", 15))
        self.__latitudeLabel = tk.Label(self.master, text="NONE", font=("Arial", 10), fg='red')
        longitudeLabel = tk.Label(self.master, text="Long:", font=("Arial", 15))
        self.__longitudeLabel = tk.Label(self.master, text="NONE", font=("Arial", 10), fg='red')
        relationsLabel = tk.Label(self.master, text="Physical Relations:", font=("Arial", 15))
        self.__relationsLabel = tk.Label(self.master, text="NONE", font=("Arial", 10), fg='red')
        canvas1.get_tk_widget().place(relx=0.5, rely=0.1, anchor='nw')
        canvas2.get_tk_widget().place(relx=0.5, rely=0.1, anchor='ne')
        canvas3.get_tk_widget().place(relx=0.03, rely=0.65, anchor='nw')
        toolbar1.place(relx=0.52, rely=0.6, anchor='w')
        toolbar2.place(relx=0.02, rely=0.6, anchor='w')
        backButton.place(relx=0, rely=0, anchor='nw', width=130)
        socNetworkPicker.place(relx=0.2, rely=0, width=150)
        selectKeywordButton.place(relx=0.37, rely=0, anchor='nw', width=200)
        selectedSocNetwork.set("gowalla")
        clusterLabel.place(relx=0.6, rely=0.01, anchor='nw')
        self.__clusterChooser.place(relx=0.8, rely=0.01, anchor='nw', width=60)
        selectedUser.place(relx=0.45, rely=0.65, anchor='w')
        idLabel.place(relx=0.45, rely=0.7, anchor='w')
        self.__idLabel.place(relx=0.49, rely=0.69, anchor='nw')
        latitudeLabel.place(relx=0.45, rely=0.75, anchor='w')
        self.__latitudeLabel.place(relx=0.5, rely=0.74, anchor='nw')
        longitudeLabel.place(relx=0.45, rely=0.8, anchor='w')
        self.__longitudeLabel.place(relx=0.52, rely=0.79, anchor='nw')
        relationsLabel.place(relx=0.45, rely=0.85, anchor='w')
        self.__relationsLabel.place(relx=0.65, rely=0.84, anchor='nw')
        fig.canvas.callbacks.connect('pick_event', self.on_pick)
        print(f"Done mapping data. Took {round((time.perf_counter() - t), 3)} seconds")

    def showUsers(self, plot, canvas, sNetwork):
        t = time.perf_counter()
        print("Plotting data...")
        if self.__currentSocialUsers is not None:
            self.__currentSocialUsers.remove()
            canvas.draw()
        y = plot.get_ylim()
        x = plot.get_xlim()
        self.__currentSocialUsers = plot.scatter(self.__socials[sNetwork].getLongs(),
                                                 self.__socials[sNetwork].getLats(), marker='.', s=50,
                                                 c='green', alpha=0.5, label="Users")
        plot.legend(prop={"size":7})
        plot.set(xlim=x, ylim=y)
        canvas.draw()
        print(f"Done plotting data. Took {round((time.perf_counter() - t), 3)} seconds")

    def showRelations(self, plot1, plot, plot2, canvas1, canvas, canvas2, sNetwork):
        t = time.perf_counter()
        self.__currentSocialStr = sNetwork
        print("Plotting data...")
        if self.__currentSocial is not None:
            self.__currentSocial.remove()
            canvas.draw()
        self.showUsers(plot1, canvas1, sNetwork)
        y = plot.get_ylim()
        x = plot.get_xlim()
        segments = np.column_stack([self.__socials[sNetwork].getPlottableLongs(),
                                   self.__socials[sNetwork].getPlottableLats()])
        lc = LineCollection([segments], linewidths=self.__socials[sNetwork].getPlottableWeights(),
                            color='#5e69ff')
        self.__currentSocial = plot.add_collection(lc)
        plot.set(xlim=x, ylim=y)
        canvas.draw()
        self.showSummary(self.__clusterChooser.get(), canvas2, plot2)
        print(f"Done plotting data. Took {round((time.perf_counter() - t), 3)} seconds")

    def showKeywords(self, canvas1, canvas2, plot1, plot2):
        root = tk.Toplevel()
        gui = tk.Frame()
        self.__keywordButtons = []
        self.__keywordButtonValues = []
        self.__keywordButtonTitles = []
        row = 0
        col = 0
        for keyword in self.__socials[self.__currentSocialStr].getKeywords()['allKeywords']:
            self.__keywordButtonValues.append(tk.IntVar())
            self.__keywordButtonTitles.append(keyword)
            button = tk.Checkbutton(root, text=keyword,
                                    variable=self.__keywordButtonValues[len(self.__keywordButtonValues) - 1])
            self.__keywordButtons.append(button)
            button.grid(row=row, column=col, sticky=tk.W)
            if col < 10:
                col += 1
            else:
                col = 0
                row += 1
        selectAllButton = tk.Button(root, text="Select All", font=("Arial", 10), height=1,
                                               command=self.selectAllKeywords).grid(row=row + 1, column=1, sticky=tk.W)
        deselectAllButton = tk.Button(root, text="Deselect All", font=("Arial", 10), height=1,
                                      command=self.deselectAllKeywords).grid(row=row + 1, column=2, sticky=tk.W)
        displayButton = tk.Button(root, text="Display Keywords", font=("Arial", 10), height=1,
                                  command=lambda *args: self.displayKeywords(canvas1, canvas2, plot1, plot2)).grid(row=row + 1, column=3,
                                                                                                 sticky=tk.W)
        closeButton = tk.Button(root, text="Close", font=("Arial", 10), height=1,
                                command=lambda: root.destroy()).grid(row=row + 1, column=4, sticky=tk.W)
        gui.mainloop()

    def showSummary(self, value, canvas, plot):
        t = time.perf_counter()
        y = plot.get_ylim()
        x = plot.get_xlim()
        print("Plotting data...")
        if self.__currentSummary is not None:
            self.__currentSummary.remove()
            canvas.draw()
        kmeans = KMeans(n_clusters=int(value))
        kmeans.fit(self.__socials[self.__currentSocialStr].getCoordList())
        centers = kmeans.cluster_centers_
        ref = list(Counter(kmeans.labels_).values())
        refSorted = list(Counter(kmeans.labels_).values())
        refSorted.sort()
        sizes = [0] * len(centers[:, 1])
        for z in range(0, len(refSorted)):
            for q in range(0, len(ref)):
                if int(ref[q]) == int(refSorted[z]):
                    sizes[q] = refSorted[z] / 5
        self.__currentSummary = plot.scatter(centers[:, 1], centers[:, 0], c='red',
                                             s=sizes, alpha=0.5)
        plot.set(xlim=x, ylim=y)
        canvas.draw()
        print(f"Done plotting data. Took {round((time.perf_counter() - t), 3)} seconds")

    def selectAllKeywords(self):
        for check in self.__keywordButtons:
            check.select()

    def deselectAllKeywords(self):
        for check in self.__keywordButtons:
            check.deselect()

    def displayKeywords(self, canvas1, canvas2, plot1, plot2):
        t = time.perf_counter()
        selected = []
        for x in range(0, len(self.__keywordButtons) - 1):
            if self.__keywordButtonValues[x].get() == 1:
                selected.append(self.__keywordButtonTitles[x])
        sNetwork = self.__currentSocialStr
        print("Plotting data...")
        if self.__currentSocialUsers is not None:
            self.__currentSocialUsers.remove()
            canvas1.draw()
            self.__currentSocialUsers = None
        if self.__currentKeywords:
            for x in range(0, len(self.__currentKeywords)):
                self.__currentKeywords[x].remove()
            canvas1.draw()
            self.__currentKeywords = []
        y = plot1.get_ylim()
        x = plot1.get_xlim()
        for i in selected:
            self.__currentKeywords.append(plot1.scatter(self.__socials[sNetwork].getKeywords()[f"{i}.longs"],
                                                        self.__socials[sNetwork].getKeywords()[f"{i}.lats"], marker='.',
                                                        s=50, alpha=0.5, label=i))
            plot1.legend(prop={"size":7})
            canvas2.draw()
        canvas1.draw()
        canvas2.draw()
        print(f"Done plotting data. Took {round((time.perf_counter() - t), 3)} seconds")

    def on_pick(self, event):
        print("User clicked")
        artist = event.artist
        ind = event.ind
        line = event.artist
        xdata, ydata = line.get_data()
        ind = event.ind
        if len(ind) > 0:
            y = np.array([xdata[ind], ydata[ind]]).T[0][0]
            x = np.array([xdata[ind], ydata[ind]]).T[0][1]
            self.__idLabel.destroy()
            self.__latitudeLabel.destroy()
            self.__longitudeLabel.destroy()
            self.__relationsLabel.destroy()
            id = self.__socials[self.__currentSocialStr].getUserByCoord(y, x)
            relations = None
            if id is not None:
                relations = self.__socials[self.__currentSocialStr].getAllRelations(float(id))
                id = int(float(id))
            else:
                relations = "NONE"
                id = "NONE"
            self.__idLabel = tk.Label(self.master, text=id, font=("Arial", 10), fg='red')
            self.__latitudeLabel = tk.Label(self.master, text=x, font=("Arial", 10), fg='red')
            self.__longitudeLabel = tk.Label(self.master, text=y, font=("Arial", 10), fg='red')
            self.__relationsLabel = tk.Label(self.master, text=relations, font=("Arial", 10), fg='red')
            self.__idLabel.place(relx=0.49, rely=0.69, anchor='nw')
            self.__latitudeLabel.place(relx=0.5, rely=0.74, anchor='nw')
            self.__longitudeLabel.place(relx=0.52, rely=0.79, anchor='nw')
            self.__relationsLabel.place(relx=0.65, rely=0.84, anchor='nw')
