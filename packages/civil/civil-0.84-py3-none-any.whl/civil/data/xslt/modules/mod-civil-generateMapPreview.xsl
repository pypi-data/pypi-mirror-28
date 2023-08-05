<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Template to generate mapPreview data from input stream...                   -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- Version     :    0.1                                                                         -->
<!--                                                                                              -->
<!-- History     :    0.1 - (25/07/01) - Initial version just to start outputting content...      -->
<!--                                                                                              -->    
<!-- ******************************************************************************************** -->

<xsl:variable name="colours" select="document('../scenario2html/colour-map.xml')"/>
<xsl:key name="hexInRow" match="hex" use="@y"/>

<!-- Ok, this is still work in progress. I've got Xalan outputting the correct colour information... -->

<!-- ******************************************************************************************** -->
<!-- Description:
       Grabs the map node, and sets up the basic table for the preview...                         -->
<!-- ******************************************************************************************** -->
<xsl:template match="map">
  <H2>Map</H2>
  <P>The table below shows a rough guide to the terrain the battle will be fought upon. </P>
  <P><B>Note:</B> Both players' starting positions have been hidden from this view...</P>
  <TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0" FRAME="VOID" ALIGN="CENTER">
    <TR>
      <TH COLSPAN="{@ysize}">Map Preview...</TH>
    </TR>
    <xsl:apply-templates/>
  </TABLE>

</xsl:template>



<!-- ******************************************************************************************** -->
<!-- Description:
       Grabs the hexes parent node, strips relevant data, and starts a recursive build of the 
       preview table...                                                                           -->
<!-- Notes: 
       The 'rows' variable can probably be global, instead of being passed on every recurse...    -->
<!-- ******************************************************************************************** -->
<xsl:template match="hexes">
  <xsl:variable name="rows" select="//map/@ysize"/>

    <xsl:call-template name="processCell">
      <xsl:with-param name="currentRow" select="0"/>
       <xsl:with-param name="stop" select="number($rows) - 1"/>
    </xsl:call-template>

</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description (Here be dragons):
       Does a selective grab of all 'hex' elements with a y attr equal to the currentRow (this is 
       passed and incremented each recursion)... From here, each row-node is iterated over, and a 
       new table cell is created for it. 

     [Iteration]
       The current node's terrain number is grabbed, and an XPath selection is used to pick the
       icon element from the 'lookup table' [colour-map.xml] which has the same number ID as the
       current node's terrain number. Once this has been found, the table cell's style attribute 
       is created, with a CSS background-colour provided as an rgb(?,?,?) style tuple containing 
       the r,g,b attr values taken from the icon node retreived from colour-map.xml earlier...
     [Recursion]
       A quick compare of the current row verses the number of rows is done. If we've not 
       completed the table, we increment the currenRow value and call ourselves...

     Notes:
       Ok, so that's a bit hairy, but I've removed the multiple for-each iterations, and speed 
       has been improved dramatically. If someone has a better solution please tell me!

       In addtion, the population of the cells required the use of an image to pad the cell 
       dimensions, and ensure that all browsers actually _showed_ the colour in the cell (NS4!)
       so now, any files produced by this transform will need an images/ folder in the same 
       directory. Thinking about it, this might not be such a bad idea as I can then use the 
       dialog borders in the same way as I did for the website... ;-)                             -->
<!-- ******************************************************************************************** -->
<xsl:template name="processCell">
  <xsl:param name="currentRow"/>
  <xsl:param name="stop"/>
  
<!-- <xsl:if test="$DEBUG"> <xsl:value-of select="count(key('row', $currentRow))"/> </xsl:if>-->

  <TR>
    <xsl:for-each select="key('hexInRow',$currentRow)">
      <TD>   
      <xsl:variable name="terrain" select="@terrain"/>
      <xsl:variable name="lookup" select="$colours/colourmap/icon[@number = $terrain]"/>
        <xsl:attribute name="STYLE">
          <xsl:text>background-color: rgb(</xsl:text>
          <xsl:value-of select="$lookup/@r"/>
          <xsl:text>,</xsl:text>
          <xsl:value-of select="$lookup/@g"/>
          <xsl:text>,</xsl:text>
          <xsl:value-of select="$lookup/@b"/>
          <xsl:text>)</xsl:text>

        </xsl:attribute>
        <img src="images/spacer.gif" width="4" height="4"/>
      </TD>
    </xsl:for-each>
  </TR>

  <xsl:if test="(number($currentRow) + 1) &lt;= $stop">
    <xsl:call-template name="processCell">
      <xsl:with-param name="currentRow" select="number($currentRow) + 1"/>
      <xsl:with-param name="stop" select="$stop"/>
    </xsl:call-template>
  </xsl:if>
  
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description:
       Suppress all the hex elements with iterated over so there's not a lot of nasty white space
       in the HTML output...                                                                      -->
<!-- ******************************************************************************************** -->

<xsl:template match="hex"/>

<!-- ******************************************************************************************** -->
     </xsl:stylesheet>
<!-- ******************************************************************************************** -->










