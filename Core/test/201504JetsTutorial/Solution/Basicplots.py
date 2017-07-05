
# here you can write down the draw functions/sequence/stuff you want to be executed with the main DrawTool.py program.
# For a complete list of all available functions and options
# please visit: https://twiki.cern.ch/twiki/bin/viewauth/CMS/CFFDrawTool

# specify if you want to run the script and ROOT in batch mode (this will not show any canvases):
#setBatchMode()

# Set the wanted input file and load all available histograms in this file in the memory:
setInput("plotsSingleJet_2016.root")
getAllHistos()

# define nice legend names for the samples that you are plotting:
setLegend("MinBias_TuneMonash13_13TeV-pythia8","Pythia8 Monash13")
setLegend("data_FSQJets3","Data")

# this will plot ALL histograms found the in the file:
draw(["jetPT"])
draw(["deltaEta"])
draw(["deltaPt"])
draw(["deltaPhi"])
draw(["hprof_cos"])
# update all open canvases to display the changes
updateCanvas()

# after drawing one can save the plots as files
# by default the PDF format is chosen to save a plot
# by default they are saved in the current directory
# save all open canvases to pdf files:
saveCanvas()
