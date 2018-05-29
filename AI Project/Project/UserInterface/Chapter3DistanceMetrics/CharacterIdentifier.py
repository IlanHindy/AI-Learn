""" Character Identifier

    The perpose of this module is to demostrate distance metrics

    The module allows to create a character set and identify an input 
    character

    The module is composed from 3 dialogs:
    -#  A main dialog (CharacterIdentifier) which present the character
        set and allow operations on this set (load, add, remove)
    -#  A dialog for entering a character (CharIdentifierInput)
    -#  A dialog to show the selection result (CharacterResolveResult)
"""

# Python Imports
import os
#from typing import

# Third party imports

# PyQt imports
from PyQt5.QtCore import QRectF, QPointF, Qt, QDataStream, QFile, QIODevice, QFileInfo, QByteArray
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QMessageBox, QGraphicsPathItem, QDialog
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QGraphicsView
from PyQt5.QtGui import QPen, QColor, QPainterPath, QBrush

# My imports
from ...PyUi.Chapter3DistanceMetrics.Ui_CharacterIdentifier import Ui_CharacterIdentifier
from ...PyUi.Chapter3DistanceMetrics.Ui_CharIdentifierInput import Ui_CharIdentifierInput
from ...PyUi.Chapter3DistanceMetrics.Ui_CharacterResolveResult import Ui_CharacterResolveResult
from ...Utilities.FileUtiles import FileUtiles
from ...AI.Chapter3DistanceMetrics import DistanceMetrics
from ...config import dataDir

# Globals - used for CharacterIdentifier
numCharCols = 5
numCharRows = 5
charPadding = 10
charWidth = 100
charHeight = 100

# Globals - used for CharIdentifierInput and CharacterResolveResults
mainItemWidth = 300
mainItemHeight = 200
mainItemPadding = 10

netColor = "white"
netThickness = 3
occupyColor = "blue"
unOccupyColor = "black"

shapeColor = "yellow"
shapeLineThickness = 5

selectedOccupiedColor = "green"
selectedShapeColor = "red"

netRows = 6
netCols = 6


class CharItem(QGraphicsRectItem):
    """ This item represents character item

        The purpose of the class is to draw a character, create a matrix
        of rectangles and resolve in which rectangles the character passes

        The class allow the following operations 
        -#  Drawing a character using the mouse events:
            -#  Start by the mouse press event
            -#  Continues by the mouse move event
            -#  The character is stored in QGraphicsPathItem
        -#  Transform the character to occupy the whole item's space
        -#  Set operation : resolving the Occupied matrix which tell on which rectangle the character
            passes
        -#  Reset operation : reverse the character transform so it is possible to continue
            drawing the character
        -#  Save operation : To a QDataStream
        -#  Load operation : From a QDataStream

        The graphical view of the class is composed from:
        -#  This class which inherits from QGraphicsRectItem and holds :
        -#  A QGraphicsPathItem : representing the character
        -#  A QGraphicsPathItem : representing the occupied rectangles
        -#  A QGraphicsPathItem : representing the unoccupied rectangles
    """

    def __init__(self, rect: QRectF, pos: QPointF, viewIndex: int=-1):
        """ CharItem constructor

            Args:
                rect    (QRectF)    : The rectangle that the character should fill
                pos     (QPointF)   : The position of the item within the parent
                viewIndex (int)     : The index of the item in case it is presented in multi character presentation
        """
        super(CharItem, self).__init__(rect)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setPresentationPrms()
        self.occupied = [[False for idx in range(self.netCols)] for idx in range(self.netRows)]
        self.charPath = None
        self.wasSetted = False
        self.occupiedPathItem = None
        self.unoccupiedPathItem = None
        self.dirty = False
        self.viewIndex = viewIndex
        self.filename = ""
        self.boundaries = rect
        self.dx = 1
        self.dy = 1
        self.posInParent = pos
        self.setPos(self.posInParent)

    def setPresentationPrms(self):
        """ Setting the presentation prms

            The reason the there is a duplicate set of presentation parameters is
            that it allows changing the presentation parameters for one character
            (like in the select option
        """

        self.netColor = netColor
        self.netThickness = netThickness
        self.occupyColor = occupyColor
        self.unOccupyColor = unOccupyColor
        self.shapeColor = shapeColor
        self.shapeLineThickness = shapeLineThickness
        self.selectedOccupiedColor = selectedOccupiedColor
        self.selectedShapeColor = selectedShapeColor
        self.netRows = netRows
        self.netCols = netCols

    def setNetBoxDimensions(self, rect: QRectF):
        """ Set net box dimensions
        
            The net box is the rectangle that compose the network
            drawn to show the occupy matrix
        """
        self.netRectHeight = rect.height() / self.netRows
        self.netRectWidth = rect.width() / self.netCols
        self.left = rect.left()
        self.top = rect.top()

    def netRect(self, row_idx: int, col_idx: int) -> QRectF:
        """ Set net rect
        
            The net box is the rectangle that compose the network
            drawn to show the occupy matrix

            Args:
                row_idx  (int)   : The row of the network rectangle
                col_idx  (int)   : The col of the network rectangle

            Returns:
                QRectF  : The rectangle
        """
        return QRectF(self.left + col_idx * self.netRectWidth, self.top + row_idx * self.netRectHeight, self.netRectWidth,
                      self.netRectHeight)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        """ Mouse move event : continue draw a line

            This event is activated when the mouse is pressed and moves

            The methods draws the line in 2 conditions:
            -# The item is not part of multi character presentation
            -# A character path was initiated (using the mouse press event)

            Args:
               event (QGraphicsSceneMouseEvent) : the event description
        """
        if self.viewIndex == -1:
            if self.charPath is not None:
                point = event.scenePos()
                path = self.charPath.path()
                path.lineTo(point)
                self.charPath.setPath(path)
                self.update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """ Mouse Press Event : Start a new line / Select the character

            If the character is part of multi character presentation 
                activate the character selection
            If the character is in single character presentation
                Start a new line in the character

            Args:
               event (QGraphicsSceneMouseEvent) : the event description
        """
        if self.viewIndex == -1:
            self.startLine(event)
        else:
            self.setSelected()

    def startLine(self, event: QGraphicsSceneMouseEvent):
        """ Start drawing a line

            When the mouse button is pressed and we are in single character
            dialog this method is activated to start drowning a line in the
            character

            Args:
               event (QGraphicsSceneMouseEvent) : the event description
        """
        # There are 2 modes for the presentation:
        # Original mode where the character is it's original size
        # After setting mode when the set was done and the character fullfill all
        # the item's space
        # Drawing can be done only in original mode
        if self.wasSetted:
            QMessageBox.critical(None, "Char identifier window", "The shape was already setted use revert setting")
            return

        # If this is the first start of a line - generate the QPainterPath and QGraphicsPathItem
        if self.charPath is None:
            self.initCharPath()

        # Move to the mouse position
        point = event.scenePos()
        path = self.charPath.path()
        path.moveTo(point)
        self.charPath.setPath(path)
        self.dirty = True

    def initCharPath(self):
        """ Init the item that holds the character

            There is one path item that holds the character
            This method is activated by start line if the char item 
            was not created to create the new and only one
        """
        self.dirty = True
        self.charPath = QGraphicsPathItem(self)
        self.charPath.setPen(QPen(QColor(self.shapeColor), self.shapeLineThickness))
        self.charPath.setZValue(1)
        self.charPath.originalPos = self.charPath.pos()
        self.charPath.setPath(QPainterPath())

    def setSelected(self):
        """ Set the item a selected item

            This method is activated when the mouse button is presses
            and the item is part of multi character presentation
        """

        # Set the colors of the item
        self.occupiedPathItem.setBrush(QBrush(QColor(self.selectedOccupiedColor)))
        self.charPath.setPen(QPen(QColor(self.selectedShapeColor), self.shapeLineThickness))
        self.update()

        # Report to the parent item about the selection
        self.parentItem().setSelected(self.viewIndex)

    def resetSelected(self):
        """ Set the colors of the item to not selected
        """

        self.occupiedPathItem.setBrush(QBrush(QColor(self.occupyColor)))
        self.charPath.setPen(QPen(QColor(self.shapeColor), self.shapeLineThickness))
        self.update()

    def set(self):
        """ Calculate the occupied matrix and present the results

            This method does the following:
            -# Fill the occupied matrix
            -# Generate the occupied and unoccupied pathes items
            -# Transform the char path to fit to the item's boundaries
        """
        # If there is no shape drawn - return
        if self.charPath is None:
            QMessageBox.critical(None, "Char identifier window", "There is no shape drawn")
            return

        # If the item is in setted mode - return
        if self.wasSetted:
            QMessageBox.critical(None, "Char identifier window", "The shape was already setted use revert setting")
            return

        # fill the occupied matrix with the data before the scaling
        self.fillOccupied()
        self.setNetBoxDimensions(self.boundingRect())
        self.createNetPaths()

        # update the transform - change the dimensions and location
        # only on the first time
        self.transformCharPath()

        self.wasSetted = True
        # update the presentation
        self.update()

    def revertTransform(self):
        """ Change from Setted mode to drawing mode

            The drawing mode is the mode where the character can be drawn
            -#  Restore the original size of the character (Reset the transform of the char item)
            -#  Restor the char path item's position to the original one (saved when created)
            -#  Empty the occupiedPath and the unoccupiedPath
        """
        # If there is no character drawn - return
        if self.charPath is None:
            QMessageBox.critical(None, "Char identifier window", "There is no shape drawn")
            return

        # If the item is already in drawing mode - return
        if not self.wasSetted:
            QMessageBox.critical(None, "Char identifier window", "The shape was not setted use set button")
            return

        # The char path item
        transform = self.charPath.transform()
        transform.reset()

        # The self.dx and self.dy are the scale parameters created when the item
        # begins and they are the scale parameters that transform it to the boundaries
        # given by the parent item
        transform.scale(self.dx, self.dy)
        self.charPath.setTransform(transform)
        self.charPath.setPos(self.charPath.originalPos)

        # Empty the network pathes
        self.occupiedPathItem.setPath(QPainterPath())
        self.unoccupiedPathItem.setPath(QPainterPath())
        self.wasSetted = False

    def transformCharPath(self):
        """ Transform char path when the item is setted

            This method does the following
            -#  scale the char path to the size of the item
            -#  calculate the new position of the char path so that it will
                be placed at the top left corner of the item
        """
        dx = self.boundingRect().width() / self.charPath.boundingRect().width()
        dy = self.boundingRect().height() / self.charPath.boundingRect().height()
        transform = self.charPath.transform()
        transform.reset()
        transform.scale(dx, dy)
        self.charPath.setTransform(transform)

        # Move the shape to the origin
        moveX = -(self.charPath.boundingRect().left() - self.boundingRect().left()) * dx
        moveY = -(self.charPath.boundingRect().top() - self.boundingRect().top()) * dy
        self.charPath.setX(self.charPath.x() + moveX)
        self.charPath.setY(self.charPath.y() + moveY)

    def fillOccupied(self):
        """ Fill the occupied matrix

            The algorithm of filling the occupied matrix is 
            -#  Scanning the char path
            -#  For each point decide on where row and column of the net
            -#  Set the occupies matrix for this column and row to True
        """

        for idx in range(100):
            point = self.charPath.path().pointAtPercent(idx / 100.)
            row_idx, col_idx = self.calcRowCol(point)
            self.occupied[row_idx][col_idx] = True

    def calcRowCol(self, point: QPointF):
        """ Calculate the network row and column that a point is int
            calc the row and column indexes of a point

            The following is the algorithm:
            1.  Find the distance between the point and the left (or top)
            2.  Divide the distance with the width of path to find the relative position
            3.  Multipile this relative position with the number of rows/cols
            4.  Convert the result to int to find the indexes
            5.  If the index is the number of row/col reduce the index
                (This is for the case the the point is on the boundary and in this
                case the relative position is 1 which will cause the indexes to
                be the number of rows/cols - out of the matrix indexes)

            Args:
                point (QPointF) : The point to resolve

            Returns:
                int : The network row that the point is in
                int : The network column that the point is in  

        """
        partialX = (point.x() - self.charPath.boundingRect().left()) / self.charPath.boundingRect().width()
        partialY = (point.y() - self.charPath.boundingRect().top()) / self.charPath.boundingRect().height()
        col_idx = int(partialX * self.netCols)
        row_idx = int(partialY * self.netRows)
        if row_idx == self.netRows:
            row_idx -= 1
        if col_idx == self.netCols:
            col_idx -= 1
        return row_idx, col_idx

    def createNetPaths(self):
        """ Create the network pathes

            This method creates 2 network pathes items one for holding
            the occupied rectangles and one to hold the unoccupied rectangles
        """
        # Generate 2 QPainterPath
        occupiedPath = QPainterPath()
        unoccupiedPath = QPainterPath()

        # For each entry in occupied matrix :
        # Add a rectangle to the appropriate path according the entry value
        for row_idx in range(self.netRows):
            for col_idx in range(self.netCols):
                if self.occupied[row_idx][col_idx]:
                    occupiedPath.addRect(self.netRect(row_idx, col_idx))
                else:
                    unoccupiedPath.addRect(self.netRect(row_idx, col_idx))

        # Create the QGraphicsPathItems that will hold the path
        self.createNetPath(self.occupyColor, occupiedPath, True)
        self.createNetPath(self.unOccupyColor, unoccupiedPath, False)

    def createNetPath(self, brushColor: str, painterPath: QPainterPath, isOccupyPathItem: bool):
        """ Create a QGraphicsPathItem for a network path
            
            Args:
                brushColor (str)            : The color for filling the rectangles
                painterPath (QPainterPath)  : The path to be inserted to the item
                isOccupyPathItem (bool)     : Whether the path is occupied or unoccupied path
        """
        # Generate the path item if not created
        if isOccupyPathItem:
            if self.occupiedPathItem is None:
                self.occupiedPathItem = QGraphicsPathItem(self)
            pathItem = self.occupiedPathItem
        else:
            if self.unoccupiedPathItem is None:
                self.unoccupiedPathItem = QGraphicsPathItem(self)
            pathItem = self.unoccupiedPathItem
        if pathItem is None:
            pathItem = QGraphicsPathItem(self)

        # Set the item parameters
        pathItem.setPath(painterPath)
        pathItem.setPen(QPen(QColor(self.netColor), self.netThickness, style=Qt.SolidLine))
        pathItem.setBrush(QBrush(QColor(brushColor)))
        pathItem.setZValue(0)

    def save(self, stream: QDataStream, filename: str):
        """ Save the item to QDataStream
            
            Args:
                stream  (QDataStream)   : The data stream to write the item to
                filename (str)          : The filename (for documenting purposes)
        """

        # The item position
        stream << self.pos()

        # The dimensions
        stream << self.rect()

        # The presentation parameters
        stream.writeQString(self.netColor)
        stream.writeQString(self.occupyColor)
        stream.writeQString(self.unOccupyColor)
        stream.writeQString(self.shapeColor)
        stream.writeInt16(self.shapeLineThickness)
        stream.writeInt16(self.netRows)
        stream.writeInt16(self.netRows)

        # The items paths
        stream << self.charPath.path()
        self.dirty = False
        self.filename = filename

    def load(self, stream, filename):
        """ Loads the item from QDataStream
            
            Args:
                stream  (QDataStream)   : The data stream to read the item from
                filename (str)          : The filename (for documenting purposes)
        """

        # read the pos
        pos = QPointF()
        stream >> pos
        self.setPos(pos)

        # read the dimensions
        rect = QRectF()
        stream >> rect
        self.setRect(rect)

        # The presentation parameters
        self.netColor = stream.readQString()
        self.occupyColor = stream.readQString()
        self.unOccupyColor = stream.readQString()
        self.shapeColor = stream.readQString()
        self.shapeLineThickness = stream.readInt16()
        self.netRows = stream.readInt16()
        self.netRows = stream.readInt16()

        # read the paths
        self.initCharPath()
        path = self.charPath.path()
        stream >> path
        self.charPath.setPath(path)

        # Fit the item to the boundaries and position given by the item's parent
        self.fitToBoundaries()

        # The presentation of the item is in setted mode so we activate the set method
        self.wasSetted = False
        self.set()

        self.dirty = False
        self.filename = filename

    def fitToBoundaries(self):
        """ Fit the item to the boundaries and position given by it's parent

            This method was made to support the change of the character
            boundaries and that the char can be presented in different
            boundaries and position
        """
        self.setPos(self.posInParent)
        self.dx = self.boundaries.width() / self.rect().width()
        self.dy = self.boundaries.height() / self.rect().height()
        transform = self.transform()
        transform.scale(self.dx, self.dy)
        self.setTransform(transform)


class CharacterIdentifier(QDialog, Ui_CharacterIdentifier):
    """Main dialog for character identifying

        The dialog allows the following operations:
        -# Load all characters in a directory (characters are files with extention chr)
        -# Select a character
        -# Activate the CharIdentifierInput to add a new character to the character set
        -# Remove the selected character
        -# Resolve a character :
            -# Activate the CharIdentifierInput for getting the character to identify
            -# Select the neerest character from the character set
            -# Present the result in CharactyerResolveResult

        The graphical structure of the dialog is :
        -#  QGraphicsView which holds a 
        -#  QGraphicsScene which holds a 
        -#  CharacterIdentifierItem (inherits from QGraphicsRectItem) which hold many
        -#  CharItem (Inherits from QGraphicsRectItem)
        
        Init results
        If the user press the cancel button when the characters input directory
        is asked when initiating the member initResults is checked
        this member should be checked before activating the dialog using exec_, exec, show 
    """

    def __init__(self, parent):
        """CharacterIdentifier constructor
        
            Args:
                parent : The parent window or dialog
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.pushButton_add.clicked.connect(self.pushButton_add_clicked)
        self.pushButton_remove.clicked.connect(self.pushButton_remove_clicked)
        self.pushButton_edit.clicked.connect(self.pushButton_edit_clicked)
        self.pushButton_resolve.clicked.connect(self.pushButton_resolve_clicked)
        self.pushButton_reload.clicked.connect(self.pushButton_reload_clicked)
        self.pushButton_exit.clicked.connect(self.accept)
        showResult, sceneWidth, sceneHeight = self.showAllCharacters()

        # Checking the self.initResult will show if the init succeeded
        # If the init succeeded the calling method should activate
        # the exec_ method
        if showResult:
            self.setFixedSize(sceneWidth + 45, sceneHeight)
            self.initResult = True
        else:
            self.initResult = False

    def showAllCharacters(self):
        """ Show all characters

            This method create the scene and fill it with the characters

            Returns:
                bool    : Wether the retrieve failed or denied by the user
                int     : Scene width
                int     : Scene height
        """
        # Create the scene
        self.graphicsScene = QGraphicsScene()
        sceneWidth = charPadding + numCharCols * (charWidth + charPadding)
        sceneHeight = charPadding + numCharRows * (charHeight + charPadding)
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsScene.setSceneRect(0, 0, sceneWidth, sceneHeight)

        # Create the main item and fill it with the characters
        self.mainItem = CharacterIdentifierItem(QRectF(0, 0, sceneWidth, sceneHeight))
        self.graphicsScene.addItem(self.mainItem)
        if self.retrieveCharacters():
            return True, sceneWidth, sceneHeight
        else:
            return False, 0, 0

    def retrieveCharacters(self) -> bool:
        """ Retrieve the character set

            The character set is a list of files with the extention chr
            in the directory that will be selected by the user in this method

            Returns:
                bool : True is the user selected a source directory
        """

        # Retrieve the directory
        fileDirectory = os.path.join(dataDir, "Chapter 3 - Distance Metrics")
        dir = QFileDialog.getExistingDirectory(self, "Open Directory", fileDirectory, QFileDialog.ShowDirsOnly
                                               | QFileDialog.DontResolveSymlinks)

        if dir == "":
            return False

        # Retrieve all the files in the directory
        charFiles = FileUtiles.GetAllFilesInFolder(dir, False, "chr")

        # Show the files
        for charFile in charFiles:
            charFile = dir + '/' + charFile
            self.mainItem.addCharacter(charFile)
        self.graphicsScene.update()
        return True

    def pushButton_add_clicked(self):
        """ Slot : Add a new character to the character set

            Activate the CharIdentifierInput dialog and
            add the new character to the main item

        """
        charIdentifierInput = CharIdentifierInput(self)
        if (charIdentifierInput.exec_()):
            if charIdentifierInput.filename:
                self.mainItem.addCharacter(charIdentifierInput.filename)
        self.graphicsScene.update()

    def pushButton_remove_clicked(self):
        """ Slot : Remove the selected character

            -#  If there is a selected character ask the user if he wants
                to remove the file also. 
            -#  Call the removeItem of the main item
        """

        if self.mainItem.selectedItemIndex == -1:
            QMessageBox.critical(None, "Char identifier window", "No item was selected")
            return

        deleteFile = QMessageBox.question(
            None, "Char Identifier Input", "Do You want to delete the character file ?",
            QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes

        self.mainItem.removeItem(deleteFile)
        self.graphicsScene.update()

    def pushButton_edit_clicked(self):
        """ Slot : edit an item

            -#  If there is a selected item call CharIdentifierInput with the filename
                of the selected character which will cause the dialog to start with the
                selected character

            -#  If the dialog returned with OK - replace the character by calling the mainItem's
                replaceCharacter method
        """
        if self.mainItem.selectedItemIndex == -1:
            QMessageBox.critical(None, "Char identifier window", "No item was selected")
            return

        charItem = self.mainItem.selectedItem()
        charIdentifierInput = CharIdentifierInput(self, charItem.filename)
        if (charIdentifierInput.exec_()):
            self.mainItem.replaceSelected(charIdentifierInput.mainItem.filename)

    def pushButton_resolve_clicked(self):
        """ Slot : resolve a character

            This method does the following :
            -#  Get a character item (using CharIdentifierInput dialog)
            -#  Resolve the neerest character (using the select method of the DistanceMetrics)
            -#  Present the result of the selection (using the CharacterResolveResult dialog)
        """
        # Get the character to identify
        charIdentifierInput = CharIdentifierInput(self)
        if (charIdentifierInput.exec_()):
            itemToResolve = charIdentifierInput.mainItem
            itemParameters = [str(boolean) for row in itemToResolve.occupied for boolean in row]
        else:
            return

        # Find the character identified
        items = [optionItem for optionItem in self.mainItem.childItems()]
        options = [[str(boolean) for row in optionItem.occupied for boolean in row] for optionItem in items]

        distanceMetrics = DistanceMetrics()
        prmOptions = [["False", "True"] for idx in range(len(options[0]))]
        optionSelected = distanceMetrics.select(prmOptions, options, itemParameters)

        # Present the results
        characterResolveResult = CharacterResolveResult(self, itemToResolve, items[optionSelected])
        characterResolveResult.exec_()

    def pushButton_reload_clicked(self):
        """ Slot : reload a character set
        """
        self.showAllCharacters()


class CharacterIdentifierItem(QGraphicsRectItem):
    """ Main item for the CharacterIdentifierDialog

        This item is composed from many CharItem
    """

    def __init__(self, rect: QRectF):
        """ CharacterIdentifierItem constructor
        """

        super(CharacterIdentifierItem, self).__init__(rect)
        self.setPos(0, 0)
        self.selectedItemIndex = -1
        self.insertionIndex = -1

    def addCharacter(self, charFile: str):
        """ Add a character to the item

            Args:
                charFile (str) : the name of the character file
        """

        self.insertionIndex += 1
        fh = QFile(charFile)
        fh.open(QIODevice.ReadOnly)
        stream = QDataStream(fh)
        itemPos = self.positionChar()
        item = CharItem(QRectF(0, 0, charWidth, charHeight), itemPos)
        item.viewIndex = self.insertionIndex
        item.setParentItem(self)
        item.load(stream, charFile)

    def positionChar(self) -> QPointF:
        """ Set the position of a char item

            returns:
                QPointF : The position to put the char path it
        """
        # Find the row and column of the insertion position of the next char item
        row = int(self.insertionIndex / numCharCols)
        col = self.insertionIndex % numCharCols

        # The position is a multiply of the row/column with the width/height of the char item
        return QPointF(self.boundingRect().left() + charPadding + col * (charWidth + charPadding),
                       self.boundingRect().top() + charPadding + row * (charHeight + charPadding))

    def removeItem(self, deleteFile: bool):
        """ Remove a char item from the presentation

            Args:
                deleteFile (bool) : whether to delete the file of the char item
        """

        # find the selected item
        charItem = self.selectedItem()

        # remove the item from the presentation
        charItem.setParentItem(None)

        # rearrange the items
        self.insertionIndex = -1
        for charItem in self.childItems():
            self.insertionIndex += 1
            self.positionChar(charItem)

        # reset the selected index
        self.selectedItemIndex = -1

        # delete the character file if requested
        if deleteFile == QMessageBox.Yes:
            fh = QFile(charItem.filename)
            fh.remove()

    def selectedItem(self) -> CharItem:
        """ Get the selected char item

            Returns:
                CharItem : The item which is selected
        """
        # Each CharItem has a view index which tells it's index in the presentation
        # In order to find the selected item we search the char items for the viewIndex
        # equals to the selected index
        for charItem in self.childItems():
            if charItem.viewIndex == self.selectedItemIndex:
                return charItem

    def setSelected(self, selectedItemIndex: int):
        """ Set the selected index
            
            The selection is done by catching left mouse button event of
            the char item. it then calls this method in order to set the selected index
            of this class
            before setting the index the different coloring of the previous selected item has to
            return to regular colors this is done by calling the resetSelected method of the char item
        """
        if self.selectedItemIndex != -1:
            charItem = self.selectedItem()
            charItem.resetSelected()
        self.selectedItemIndex = selectedItemIndex

    def replaceSelected(self, filename: str):
        """ Replace the selected item (with an edited one)

            After editing an item the old item in the presentation has to be
            replaced with the new one

            Args:
                filename (str) : the name of the file of the new char item
        """
        self.insertionIndex = self.selectedItemIndex - 1
        charItem = self.selectedItem()
        charItem.setParentItem(None)
        self.addCharacter(filename)


class CharIdentifierInput(QDialog, Ui_CharIdentifierInput):
    """ Get a character

        A dialog for creating / getting a character

        The followings are the operations in the dialog
        -#  Painting a character
        -#  Set : analyze the character drawn which is composed from the following stages
            -#  Transform the character to the size of the main item
            -#  Draw a network composed from squares
            -#  Decide which squares are occupied by the character
        -#  Save : Saves the character
        -#  Load : Loads the character from file
        -#  Cancel : exit and retrun False
        -#  OK : exit and return True

        Graphical structure of the dialog
        -# Vertical box layout
        -#   Buttons horizontal layout
        -#   GraphicsView which holds a
        -#   Graphics scene which hols a
        -#   CharItem
       
    """

    def __init__(self, parent, filename: str=None):
        """CharIdentifierInput constructor
        
            Args:
                parent : The parent window or dialog
                filename : The character will be loaded from the file
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(mainItemWidth + 2 * mainItemPadding + 40, mainItemHeight + 2 * mainItemPadding + 60)
        self.createGui()
        self.pushButton_set.clicked.connect(self.pushButton_set_clicked)
        self.pushButton_save.clicked.connect(self.pushButton_save_clicked)
        self.pushButton_load.clicked.connect(self.pushButton_load_clicked)
        self.pushButton_cancel.clicked.connect(self.reject)
        self.pushButton_OK.clicked.connect(self.accept)
        self.pushButton_reset.clicked.connect(self.pushButton_reset_clicked)
        self.pushButton_revertSet.clicked.connect(self.pushButton_revertSet_clicked)
        self.dirty = False
        self.filename = filename
        if filename:
            self.pushButton_load_clicked(filename)

    def createGui(self):
        """ Create the scene and the new item
        """
        self.graphicsScene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsScene)
        self.itemBoundaries = QRectF(0, 0, mainItemWidth, mainItemHeight)
        self.itemPos = QPointF(mainItemPadding + 3, mainItemPadding)
        self.graphicsScene.setSceneRect(0, 0, mainItemWidth + 2 * mainItemPadding, mainItemHeight + 2 * mainItemPadding)
        self.newItem()

    def newItem(self):
        """ Create new main item
        """
        self.mainItem = CharItem(self.itemBoundaries, self.itemPos)
        self.graphicsScene.addItem(self.mainItem)

    def pushButton_set_clicked(self):
        """ Activate the set operation of the main item
        """
        self.mainItem.set()

    def pushButton_save_clicked(self):
        """ Slot : Activate the save operation
        """
        # If there where no changes - return
        if not self.mainItem.dirty:
            QMessageBox.critical(None, "Character Identifier - Save", "Nothing to save")
            return

        # Get the previous filename and path
        path = QFileInfo(self.filename).path() if self.filename else os.path.join(dataDir,
                                                                                  "Chapter 3 - Distance Metrics")
        fname = QFileDialog.getSaveFileName(self, "Character Identifier - Save", path,
                                            "Character Identifier Files (*.chr)")

        # If the user pressed the cancel button in the dialog - return
        if not fname:
            return
        if not fname[0].lower().endswith(".chr"):
            fname[0] += ".chr"
        self.filename = fname[0]

        try:
            # Open the file create the stream and activate the save method of the
            # main item
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(fh.errorString())
            stream = QDataStream(fh)
            self.mainItem.save(stream, self.filename)

        except IOError as e:
            QMessageBox.warning(self, "Character Identifier -- Save Error", "Failed to save {}: {}".format(
                self.filename, e))
        finally:
            if fh is not None:
                fh.close()

    def pushButton_load_clicked(self, filename: str=None):
        """ Slot : Activate the load from file operation
        """

        # If the character was not loaded from a file and no save was done
        if not self.filename:
            self.save()
            path = QFileInfo(self.filename).path() if self.filename else os.path.join(
                dataDir, "Chapter 3 - Distance Metrics")
            fname = QFileDialog.getOpenFileName(self, "Character Identifier - Open", path,
                                                "Character Identifier Files (*.chr)")
            if not fname:
                return
            self.filename = fname[0]
            fh = None
        else:
            self.filename = filename

        try:
            fh = QFile(self.filename)

            if not fh.open(QIODevice.ReadOnly):
                raise IOError(fh.errorString())
            items = self.graphicsScene.items()
            while items:
                item = items.pop()
                self.graphicsScene.removeItem(item)
                del item

            stream = QDataStream(fh)
            self.mainItem = CharItem(self.itemBoundaries, self.itemPos)
            self.graphicsScene.addItem(self.mainItem)
            self.mainItem.load(stream, self.filename)
            self.dirty = False
        except IOError as e:
            QMessageBox.warning(self, "Page Designer -- Open Error", "Failed to open {}: {}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()

    def accept(self):
        """ Slot : OK exit
        """
        # If the item was not set - set it
        if not self.mainItem.wasSetted:
            self.mainItem.set()

        # Save the item
        self.save()
        return super(CharIdentifierInput, self).accept()

    def save(self):
        """ save operation

            This method is activated before all the operations that cause
            The item to be removed from the screen
        """
        # If the item was changed - ask for saving
        if self.mainItem.dirty:
            if QMessageBox.question(None, "Char Identifier Input", "Do You want to save changes ?",
                                    QMessageBox.StandardButtons(QMessageBox.Yes
                                                                | QMessageBox.No)) == QMessageBox.Yes:
                self.pushButton_save_clicked()

    def reject(self):
        """ Slot : reject operation

            exit the dialog with true
        """
        self.save()
        return super(CharIdentifierInput, self).accept()

    def pushButton_reset_clicked(self):
        """ Slot : clear the presentation
        """
        self.save()
        self.graphicsScene.clear()
        self.graphicsView.viewport().update()
        self.newItem()

    def pushButton_revertSet_clicked(self):
        """ Slot : revert the setting for continue drowning
        """
        self.mainItem.revertTransform()


class CharacterResolveResult(QDialog, Ui_CharacterResolveResult):
    """ A dialog for showing the results of the resolve
    
        The dialog shows the character to resolve aside the selected result

        The dialog has no operations except exit

        The graphical view of the dialog is:
        -#  Vertical box layout holds 
        -#  2 QGraphicsView which holds 
        -#  A QGraphicsScene which holds 
        -#  A CharItem

    """

    def __init__(self, parent, characterToResolve: CharItem, selectedCharacter: CharItem):
        """ CharacterResolveResult constructor

            Args:
                parent  : The parent window
                characterToResolv   (CharItem)  :   The character to resolve
                selectedCCharacter  (CharItem)  :   The selected character
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.characterToResolve = characterToResolve
        self.selectedCharacter = selectedCharacter
        self.graphicsScene_characterToResolve = self.addItem(self.graphicsView_characterToResolve, characterToResolve)
        self.graphicsScene_selectedCharacter = self.addItem(self.graphicsView_selectedCharacter, selectedCharacter)
        self.setFixedSize(self.graphicsScene_characterToResolve.sceneRect().width() * 2 + 30,
                          self.graphicsScene_characterToResolve.sceneRect().height() + 80)
        self.label_selectedCharacter.setText("Selected Character (" + os.path.basename(selectedCharacter.filename) +
                                             ")")

    def addItem(self, graphicsView: QGraphicsView, item: CharItem) -> QGraphicsScene:
        """ Add Item to one of the 2 windows

            Args:
                graphicsView (QGraphicsView): The graphics view to put the item in
                item         (CharItem)     : The char item to put in the view

            Returns:
                QGraphicsScene  : The graphics scene created for the view
        """

        scene = QGraphicsScene()
        graphicsView.setScene(scene)
        newItem = CharItem(QRectF(0, 0, mainItemWidth, mainItemHeight), QPointF(mainItemPadding, mainItemPadding))
        copiedItem = QByteArray()
        stream = QDataStream(copiedItem, QIODevice.WriteOnly)
        item.save(stream, item.filename)
        stream = QDataStream(copiedItem, QIODevice.ReadOnly)
        newItem.load(stream, item.filename)
        scene.addItem(newItem)
        scene.setSceneRect(0, 0, mainItemWidth + 2 * mainItemPadding + 6, mainItemHeight + 2 * mainItemPadding)
        return scene
