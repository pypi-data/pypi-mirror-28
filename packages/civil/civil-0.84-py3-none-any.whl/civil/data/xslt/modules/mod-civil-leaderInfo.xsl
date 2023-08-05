<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Echos out the leader info. Supressing all the good bits! ;-)                -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- Version     :    0.1                                                                         -->
<!--                                                                                              -->
<!-- History     :    0.1 - (04/08/01) - Initial version just to start outputting content...      -->
<!--                                                                                              -->
<!-- Notes       :    I dropped me pen...                                                         -->    
<!-- ******************************************************************************************** -->


<!-- ******************************************************************************************** -->
<!-- Description:
       Sets up the rebel units template... Adds some colour (etc..)                               -->
<!-- ******************************************************************************************** -->

<xsl:template match="units/rebel">
  <H2>Confederate Commanders:</H2>
  <P>The following commanders are leading the confederate troups, their stats are displayed below... </P>
  <TABLE frame="VOID" cellpadding="2" cellspacing="1" valign="MIDDLE" border="0" STYLE="background-color: #eeeeee" ALIGN="CENTER">
    <TR>
      <TH>
        Commander's<BR/>Name
      </TH>
      <TH>
        Experience
      </TH>
      <TH>
        Aggressiveness
      </TH>
      <TH>
        Rally<BR/>Rating
      </TH>
      <TH>
        Motivation<BR/>Rating
      </TH>
    </TR>
    <xsl:apply-templates/>
  </TABLE>
</xsl:template>


<!-- ******************************************************************************************** -->
<!-- Description:
       Populate the leader table for rebels...                                                    -->
<!-- ******************************************************************************************** -->


<xsl:template match="units/rebel//commander">
  <TR>
    <TD ALIGN="RIGHT">
      <B>
        <xsl:value-of select="./@name"/>
      </B>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::experience/@value"/>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::aggressiveness/@value"/>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::rally/@value"/>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::motivation/@value"/>
    </TD>
  </TR>
</xsl:template>

<!-- ******************************************************************************************** -->
<!--  Description:
        Setup the table for union leaders, add some colour etc...                                 -->
<!-- ******************************************************************************************** -->

<xsl:template match="units/union">
  <H2>Union Commanders:</H2>
  <P>The following commanders are leading the union troups, their stats are shown below:</P>
  <TABLE frame="VOID" cellpadding="2" cellspacing="1" valign="MIDDLE" border="0" STYLE="background-color: #eeeeFF" ALIGN="CENTER">
    <TR>
      <TH>
        Commander's<BR/>Name
      </TH>
      <TH>
        Experience
      </TH>
      <TH>
        Aggressiveness
      </TH>
      <TH>
        Rally<BR/>Rating
      </TH>
      <TH>
        Motivation<BR/>Rating
      </TH>
    </TR>
    <xsl:apply-templates/>
  </TABLE>
</xsl:template>


<!-- ******************************************************************************************** -->
<!-- Description:
       Populates the leader table for unions...                                                   -->
<!-- ******************************************************************************************** -->


<xsl:template match="units/union//commander">
  <TR>
    <TD ALIGN="RIGHT">
      <B>
        <xsl:value-of select="./@name"/>
      </B>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::experience/@value"/>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::aggressiveness/@value"/>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::rally/@value"/>
    </TD>
    <TD ALIGN="CENTER">
        <xsl:value-of select="descendant::motivation/@value"/>
    </TD>
  </TR>
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description:
       Suppress all the stuff we don't want from the leaders info. Removes some whitespace from 
       the output...                                                                              -->
<!-- ******************************************************************************************** -->

<xsl:template match="headquarter"/>
<xsl:template match="pos"/>
<xsl:template match="men"/>
<xsl:template match="morale"/>
<xsl:template match="fatigue"/>
<xsl:template match="experience"/>
<xsl:template match="facing"/>


<!-- ******************************************************************************************** -->
     </xsl:stylesheet>
<!-- ******************************************************************************************** -->


