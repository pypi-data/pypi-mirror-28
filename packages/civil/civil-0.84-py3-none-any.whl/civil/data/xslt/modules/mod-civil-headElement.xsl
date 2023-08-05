<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Module for the inclusion of heading and CSS elements in the output HTML...  -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- Version     :    0.1                                                                         -->
<!--                                                                                              -->
<!-- History     :    0.1 - (25/07/01) - First version...                                         -->
<!-- ******************************************************************************************** -->

<!-- ******************************************************************************************** -->
<!-- Description: 
       Explicitly called tamplate; echos out a CSS link and some Title information...             -->
<!-- ******************************************************************************************** -->

<xsl:template name="mod-civil-headElement">
   <HEAD>
     <TITLE>Scenario No.: <xsl:value-of select="/scenario/scenarioinfo/@id"/> - Name: <xsl:value-of select="/scenario/scenarioinfo/name"/></TITLE>
     <LINK HREF="scenario-style.css" REL="Stylesheet" TYPE="text/css"/> 	
  </HEAD> 
</xsl:template>

<!-- ******************************************************************************************** -->
</xsl:stylesheet>
<!-- ******************************************************************************************** -->
