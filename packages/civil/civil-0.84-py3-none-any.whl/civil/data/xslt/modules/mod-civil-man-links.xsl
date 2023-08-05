<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Module for the conversion of DocBook IDRefs and links to XHTML              -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- ******************************************************************************************** -->

<xsl:template match="chapter | sect1 | appendix">
  <xsl:choose>
    <xsl:when test="@id">
      <a href="#" name="{@id}"/>
      <xsl:apply-templates/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="xref">
  <a href="#{@linkend}"><xsl:value-of select="@linkend"/></a>
</xsl:template>

<!-- ******************************************************************************************** -->
</xsl:stylesheet>
<!-- ******************************************************************************************** -->
