<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Template for the transformation of the Civil Docbook manual to XHTML        -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!--                                                                                              -->
<!-- History     :                                                                                -->
<!--                                                                                              -->
<!-- Notes       :                                                                                -->
<!-- ******************************************************************************************** -->

<!-- Force XHTML doctype output                                                                   -->

<xsl:output method="html" indent="no" encoding="iso-8859-1" doctype-system="XHTML-Transitional.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" />


<!-- ******************************************************************************************** -->
<!-- Module Import Declarations...                                                                -->
<!--       These modules do all the real work. See each file for comments...                      -->
<!-- ******************************************************************************************** -->

<xsl:include href="../modules/mod-civil-man-headings.xsl"/>
<xsl:include href="../modules/mod-civil-man-bodyContent.xsl"/>
<xsl:include href="../modules/mod-civil-man-links.xsl"/>
<xsl:include href="../modules/mod-civil-man-faq.xsl"/>


<!-- ******************************************************************************************** -->
<!-- Description :                                                                                -->
<!--       Base template, matches the root of the imcoming stream and sets-up the XHTML document, -->
<!--       it's style sheet and any other misc info...                                            -->
<!-- ******************************************************************************************** -->

<xsl:template match="/">
    <html>
      <head>
        <title>Civil Playing manual</title>
        <link href="manual-style.css" rel="Stylesheet" type="text/css"/> 
      </head>

      <body>
        <xsl:apply-templates/>
      </body>
    </html>
  </xsl:template>

<!-- ******************************************************************************************** -->
</xsl:stylesheet>
<!-- ******************************************************************************************** -->






