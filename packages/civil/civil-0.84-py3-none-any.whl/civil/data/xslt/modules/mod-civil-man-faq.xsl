<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Module for the conversion of DocBook QandA to some XHTML format...          -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- ******************************************************************************************** -->

<xsl:template match="appendix">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="qandaentry">
  <div class="qanda"><xsl:apply-templates/></div>
</xsl:template>

<xsl:template match="question">
  <h3 class="question"><xsl:value-of select="./para"/></h3>
</xsl:template>

<xsl:template match="answer">
  <blockquote class="answer"><xsl:apply-templates/></blockquote>
</xsl:template>

<xsl:template match="question/para | answer/para">
  <xsl:apply-templates/>
</xsl:template>

<!-- ******************************************************************************************** -->
</xsl:stylesheet>
<!-- ******************************************************************************************** -->
