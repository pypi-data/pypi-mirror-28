<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Module for the conversion of DocBook body elements to XHTML...              -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- ******************************************************************************************** -->


<!-- ******************************************************************************************** -->
<!-- Body tags...                                                                                 -->
<!-- ******************************************************************************************** -->

<xsl:template match="//para">
   <p><xsl:apply-templates/></p>
</xsl:template>

<xsl:template match="itemizedlist">
  <ol><xsl:apply-templates/></ol>
</xsl:template>

<xsl:template match="listitem">
   <li>
      <xsl:apply-templates/>
   </li>
</xsl:template>

<xsl:template match="screen">
  <pre><xsl:apply-templates/></pre>
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Character Level Formatting...                                                                -->
<!-- ******************************************************************************************** -->

<xsl:template match="emphasis">
  <em><xsl:value-of select="."/></em>
</xsl:template>

<xsl:template match="keycode">
  <b class="key"><xsl:value-of select="."/></b>
</xsl:template>

<xsl:template match="guimenuitem">
  <b class="gui"><xsl:value-of select="."/></b>
</xsl:template>

<xsl:template match="guibutton">
  <b class="gui"><xsl:value-of select="."/></b>
</xsl:template>

<xsl:template match="firstterm">
  <b class="firstterm"><xsl:value-of select="."/></b>
</xsl:template>

<xsl:template match="prompt">
  <b><xsl:value-of select="."/></b>
</xsl:template>

<xsl:template match="userinput">
  <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="filename">
  <b class="filename"><xsl:value-of select="."/></b>
</xsl:template>

<!-- ******************************************************************************************** -->
</xsl:stylesheet>
<!-- ******************************************************************************************** -->
