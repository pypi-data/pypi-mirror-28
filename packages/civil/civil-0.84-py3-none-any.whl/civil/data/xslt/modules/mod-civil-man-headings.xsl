<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Module for the conversion of DocBook Heading Levels to XHTML versions       -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- ******************************************************************************************** -->


<!-- ******************************************************************************************** -->
<!-- Headings...                                                                                  -->
<!-- ******************************************************************************************** -->
<xsl:template match="title">
  
  <xsl:if test="parent::bookinfo">
    <h1 class="book"><xsl:value-of select="."/></h1>
  </xsl:if>

  <xsl:if test="parent::chapter">
    <h1 class="chapter"><xsl:value-of select="."/></h1>
  </xsl:if>

  <xsl:if test="parent::appendix">
    <h1 class="appendix"><xsl:value-of select="."/></h1>
  </xsl:if>

  <xsl:if test="parent::sect1">
    <h2 class="sect1"><xsl:value-of select="."/></h2>
  </xsl:if>

  <xsl:if test="parent::sect2">
    <h3 class="sect2"><xsl:value-of select="."/></h3>
  </xsl:if>

  <xsl:if test="sect3">
    <h4 class="sect3"><xsl:value-of select="."/></h4>
  </xsl:if>

</xsl:template>
<!-- ******************************************************************************************** -->
</xsl:stylesheet>
<!-- ******************************************************************************************** -->
