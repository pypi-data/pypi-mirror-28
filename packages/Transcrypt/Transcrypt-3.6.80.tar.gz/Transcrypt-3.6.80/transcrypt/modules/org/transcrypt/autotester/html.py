# File: autotester/html.py
# Author: Carl Allendorph
# Date: 20NOV2016
#
# Description:
#   This file contains the HTML generation code for the autotester.
# This includes generating the initial HTML file as output of the
# python run, and the javascript that builds the results at runtime
# in the browser.
#

from org.transcrypt.stubs.browser import __main__, __envir__, __pragma__

__pragma__ ('nokwargs')

okColor = 'green'
errorColor = 'red'
highlightColor = 'yellow'
testletNameColor = 'blue'

messageDivId = 'message'
referenceDivId = 'python'
refResultDivId = "pyresults"
refPosDivId = "pypos"
testDivId = 'transcrypt'
tableId = 'resulttable'
resultsDivId = 'results'
faultRowClass = 'faultrow'
testletHeaderClass = "testletheader"
transValClass = "trans-val"
transPosClass = "trans-pos"
pyValClass = "py-val"
pyPosClass = "py-pos"
excAreaId = "exc-area"
excHeaderClass = "exc-header"
forceCollapseId = "force-collapse"
forceExpandId = "force-expand"

class HTMLGenerator(object):
	""" This class generates the HTML template for the autotester results.
	This code is primarily run during the Python execution cycle but
	does define strings that are referenced by the javascript as well.
	"""
	def __init__(self, filenameBase = None):
		"""
		@param filenameBase string denoting the base filename for the
		files this class will generate. This should NOT include the
		file extension (.html for example). This will be tacked on
		later depending on minified state.
		"""
		self._fnameBase = filenameBase

	def generate_html(self, refDict, minified = False):
		""" Generate the HTML file that gets generated by the
		Python script portion of the test. File will be named
		'<fnameBase.html'
		@param refDict Dict of python reference data associated with
		  each of the test modules. The keys of this dict are the names
		  of the ref modules.
		@param minified indicates whether the output file should use the
		  minified version of the javascript or not. If minified, then
		  the output file will be name 'fnameBase.min.html'
		"""
		if ( self._fnameBase is None ):
			raise ValueError("Filename Base must be defined to generate")
		minInfix = '.min' if minified else ''
		fname = minInfix.join([self._fnameBase, '.html'])
		jsFileName = minInfix.join([self._fnameBase, '.js'])
		jsPath = "{}/{}".format(__envir__.target_subdir, jsFileName)

		with open( fname, 'w') as f:
			f.write("<html><head>")
			self._writeCSS(f)
			f.write("</head><body>")

			self._writeStatusHeaderTemplate(f)

			dc = DataConverter()
			dc.writeHiddenResults(f, refDict)

			self._writeTableArea(f)

			f.write ('<script src="{}"></script>\n\n'.format (jsPath))
			f.write("</body></html>")

	##########################
	# Internal Methods
	##########################

	def _writeCSS(self, f):
		cssOut = """
		<style>
		  body {
		    max-width: 100%;
		  }
		  .faultrow > td {
		     background-color: LightCoral;
		  }
		  #resulttable {
		    border-collapse: collapse;
		    width: 100%;
		    table-layout: fixed;
		  }
		  #resulttable th, #resulttable td {
		    border: 1px solid grey;
		  }
		  .testletheader > td {
		    background-color: LightSkyBlue;
		  }
		  .header-pos {
		    width: 20%;
		  }
		  .header-val {
		    width: 30%;
		  }
		  .py-pos,.trans-pos {
		    width: 20%;
		    overflow: hidden;
		  }
		  .py-val, .trans-val {
		    width: 30%;
		    overflow-x: auto;
		  }
		  .exc-header {
	      color: red;
		  }
		  .collapsed {
		    display: None;
		  }
		</style>
		"""
		f.write(cssOut)

	def _writeStatusHeaderTemplate(self, f):
		f.write ('<b>Status:</b>\n')
		f.write ('<div id="{}"></div><br><br>\n\n'.format (messageDivId))

	def _writeTableArea(self, f):
		f.write ('<div id="{}"></div>'.format(excAreaId))
		f.write ('<div id="{}">'.format(resultsDivId))
		f.write ('<div> <a id="{}" href="#"> Collapse All</a> <a id="{}" href="#">Expand All</a></div>'.format(forceCollapseId, forceExpandId))
		f.write ('<table id="{}"><thead><tr> <th colspan="2"> CPython </th> <th colspan="2"> Transcrypt </th> </tr>'.format(tableId))
		f.write ('<tr> <th class="header-pos"> Location </th> <th class="header-val"> Value </th> <th class="header-val"> Value </th> <th class="header-pos"> Location </th> </tr></thead><tbody></tbody>')
		f.write ('</table>')
		f.write ('</div>')

class DataConverter(object):
	""" This class contains code that stores the python results in
	the HTML document and can extract the data from the HTML to
	prepare it for comparison with the javascript results.
	"""

	def writeHiddenResults(self, f, refDict):
		""" Write the Python results into a div that is hidden by
		default so that we can extract it at runtime.
		@param f file that we are writing the content into
		@param refDict python reference result data in the form of
		a dict. The keys are the names of the individual test modules.
		"""
		f.write('<div id="{}" style="display: None">'.format(referenceDivId))
		for key in refDict.keys():
			itemData = ' | '.join([x[1] for x in refDict[key]])
			posContent = ' | '.join([x[0] for x in refDict[key]])
			f.write('<div id="{}">\n'.format(key))
			# @note - we should probably HTML escape this
			#    data so that we don't get the HTML rendering
			#    engine mucking with our test result.
			f.write ('<div id="{}">{}</div>\n\n'.format (refResultDivId, itemData))
			f.write ('<div id="{}">{}</div>\n'.format(refPosDivId, posContent))
			f.write('</div>\n')
		f.write('</div></div>\n')

	def getPythonResults(self):
		""" Acquire the python unit test results from the
		    hidden div and parse into a dictionary.
		@return dict whose keys are the names of the test
		  submodules.
		"""
		refData = document.getElementById(referenceDivId)
		# Each of the children of this element is in the form
		# <div id="{key}">
		#   <div id="pyresults"> {Result Content} </div>
		#   <div id="pypos"> {Result Positions} </div>
		# </div>
		refDict = {}
		for child in refData.children:
			keyName = child.getAttribute("id")
			posData,resultData = self._extractPosResult(child)
			refDict[keyName] = zip(posData, resultData)
		return(refDict)

	def _extractPosResult(self, elem):
		resultData = None
		posData = None
		for e in elem.children:
			idStr = e.getAttribute("id")
			if ( idStr == refResultDivId):
				resultData = e.innerHTML.split(' | ')
			elif ( idStr == refPosDivId):
				posData = e.innerHTML.split(' | ')
			else:
				# Unknown Element - very strange
				pass
		return(posData, resultData)


def getRowClsName(name):
	""" Utility method for naming the test module class that
	    a row belows to
	"""
	return("mod-" + name)


class JSTesterUI(object):
	""" This class contains the code that populates the autotester results
	while running in the javascript runtime.
	"""
	def __init__(self):
		"""
		"""
		self.expander = TestModuleExpander()

	def setOutputStatus(self, success):
		if ( success ):
			document.getElementById(messageDivId).innerHTML = '<div style="color: {}">Test succeeded</div>'.format (okColor)
		else:
			document.getElementById(messageDivId).innerHTML = '<div style="color: {}"><b>Test failed</b></div>'.format (errorColor)

	def appendSeqRowName(self, name, errCount):
		"""
		"""
		table = document.getElementById(tableId)
		# Insert at the end
		row = table.insertRow(-1);
		row.id = name
		row.classList.add(testletHeaderClass)
		self.expander.setupCollapseableHeader(row, (errCount == 0))

		# Populate the Row
		headerCell = row.insertCell(0)
		headerCell.innerHTML = name + " | Errors = " + str(errCount)
		headerCell.colSpan = 4
		headerCell.style.textAlign= "center"


	def appendTableResult(self, name, testPos, testItem, refPos, refItem, collapse=False):
		clsName = getRowClsName(name)

		table = document.getElementById(tableId)
		# Insert at the end
		row = table.insertRow(-1);
		row.classList.add(clsName)
		if ( testItem != refItem ):
			row.classList.add(faultRowClass)
			refPos = "!!!" + refPos
		else:
			self.expander.setCollapsed(row, collapse)

		# Populate the Row
		cpy_pos = row.insertCell(0)
		cpy_pos.innerHTML = refPos
		cpy_pos.classList.add(pyPosClass)
		cpy_val = row.insertCell(1)
		cpy_val.innerHTML = refItem
		cpy_val.classList.add(pyValClass)
		trans_val = row.insertCell(2)
		if ( testItem is not None ):
			trans_val.innerHTML = testItem
		trans_val.classList.add(transValClass)
		trans_pos = row.insertCell(3)
		if ( testPos is not None ):
			trans_pos.innerHTML = testPos
		trans_pos.classList.add(transPosClass)


	def showException(self, testname, exc):
		"""
		"""
		excElem = document.getElementById(excAreaId)
		header = document.createElement("H2")
		header.classList.add(excHeaderClass)
		header.innerHTML = "Exception Thrown in JS Runtime";
		excElem.appendChild(header)
		content = document.createElement("p")
		content.innerHTML = "Exception in {}: {}".format(testname, str(exc))
		excElem.appendChild(content)
		stacktrace = document.createElement("p")
		if ( exc.stack is not None ):
			stacktrace.innerHTML = str(exc.stack)
		else:
			stacktrace.innerHTML = "No Stack Trace Available!"


class TestModuleExpander(object):
	""" This class handles expanding or contracting a set of
	test row results under a particular test.
	"""
	def __init__(self):
		"""
		"""
		self.collapsedClass = "collapsed"
		self.modCollapseClass = "mod-collapsed"

		self._expandCollapseAllFuncs()

	def setCollapsed(self, row, collapse):
		"""
		"""
		if ( collapse ):
			row.classList.add(self.collapsedClass)
		else:
			row.classList.remove(self.collapsedClass)


	def setupCollapseableHeader(self, row, startCollapsed = False):
		"""
		"""
		if ( startCollapsed ):
			row.classList.add(self.modCollapseClass)

		def toggleCollapse(evt):
			""" Toggle whether the
			"""
			headerRow = evt.target.parentElement
			doCollapse = not headerRow.classList.contains(self.modCollapseClass)
			self.collapseModule(headerRow, doCollapse)

		row.onclick = toggleCollapse


	def collapseModule(self, headerRow, doCollapse):
		""" collapse/expand particular module in the table of results
		"""
		name = headerRow.id
		table = document.getElementById(tableId)
		clsName = getRowClsName(name)
		allRows = table.tHead.children
		rows = filter(lambda x: x.classList.contains(clsName), allRows)

		for row in rows:
			self.setCollapsed(row, doCollapse)

		if ( doCollapse ):
			headerRow.classList.add(self.modCollapseClass)
		else:
			headerRow.classList.remove(self.modCollapseClass)

	def _expandCollapseAllFuncs(self):
		""" This function sets up the callback handlers for the
		collapse all and expand all links
		"""

		def applyToAll(evt, collapse):
			"""
			"""
			table = document.getElementById(tableId)

			# find all rows in the testletheader class
			filtFunc = lambda x: x.classList.contains(testletHeaderClass)
			headerRows = filter(filtFunc, table.tHead.children)

			for headerRow in headerRows:
				self.collapseModule(headerRow, collapse)

		def collapseAll(evt):
			""" collapse all rows handler
			"""
			evt.preventDefault()
			applyToAll(evt, True)
			return(False)

		def expandAll(evt):
			""" Expand All Rows Handler
			"""
			evt.preventDefault()
			applyToAll(evt, False)
			return(False)

		forceCollapse = document.getElementById(forceCollapseId)
		forceCollapse.onclick = collapseAll

		forceExpand = document.getElementById(forceExpandId)
		forceExpand.onclick = expandAll
