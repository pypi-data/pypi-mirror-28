<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Template for the transformation of Scenario descriptive content into plain
                 |    HTML. It's all very simple now isn't it?! ;-P                               -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- Version     :    0.1                                                                         -->
<!--                                                                                              -->
<!-- History     :    0.1 - (25/07/01) - Initial version just to start outputting content...      -->
<!--                                                                                              -->
<!-- Notes       :    We could really do with some character level formatting markup in the       -->
<!--             |    scenarios to make potentially long descriptive content a bit more purty...  -->
<!-- ******************************************************************************************** -->

<xsl:template match="scenarioinfo">
  <H1><xsl:value-of select="./name"/></H1>

  <DIV ALIGN="CENTER">
    <TABLE width="350" frame="VOID" cellpadding="2" cellspacing="1" valign="MIDDLE" border="0">
      <TR>
        <TH COLSPAN="2" CLASS="gameinfo"><xsl:value-of select="./name"/> Game Info</TH>
      </TR>
      <TR>
        <TD CLASS="gameinfohead"><B>Number of turns:</B></TD>
        <TD CLASS="gameinfo">
          <xsl:value-of select="./turns/@max"/>
        </TD>
      </TR>
      <TR>
        <TD CLASS="gameinfohead"><B>Battlefield Location:</B></TD>
        <TD CLASS="gameinfo">
          <xsl:value-of select="./location"/>
        </TD>
      </TR>
      <TR>
        <TD CLASS="gameinfohead"><B>Battle Date/Time:</B></TD>
        <TD CLASS="gameinfo">
          <xsl:value-of select="./date/@day"/>/<xsl:value-of select="./date/@month"/>/<xsl:value-of select="./date/@year"/>
          <xsl:text disable-output-escaping="yes">&amp;nbsp;&amp;#151;&amp;nbsp;</xsl:text> 
          <xsl:value-of select="./date/@hour"/>:<xsl:value-of select="./date/@minute"/>
        </TD>
      </TR>
    </TABLE> 
  </DIV>
    <H2>Overview:</H2>
    <P CLASS="description">
      <xsl:value-of select="./description/para"/>
  </P>
  <xsl:apply-templates/>
</xsl:template>


<!-- ******************************************************************************************** -->
<!-- Description:
       Noddy template to echo the missions for the players...                                     -->
<!-- ******************************************************************************************** -->

<xsl:template match="missions">
  <H3>Confederate Mission:</H3>
  <P STYLE="background-color: #eeeeee;" CLASS="mission">
    <xsl:value-of select="./rebel"/>
  </P>
  <H3>Union Mission:</H3>
  <P STYLE="background-color: #ccccFF;" CLASS="mission">
    <xsl:value-of select="./union"/>
  </P>
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description:
       Sets up a table for the contents of the weapons elements. Shows the weapons that appear in
       the game...                                                                                -->
<!-- ******************************************************************************************** -->

<xsl:template match="weapons">
  <H3>Weapons</H3>
  <P>The following weapons appear on the field of battle:</P>
  <TABLE frame="VOID" cellpadding="2" cellspacing="1" valign="MIDDLE" border="0" ALIGN="CENTER">
    <TR>
      <TH>
        Weapon Name
      </TH>
      <TH>
        Weapon Type
      </TH>
      <TH>
        Range of<BR/>Weapon
      </TH>
      <TH>
        Damage
      </TH>
    </TR>
    <xsl:apply-templates/>
  </TABLE>
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description:
       Populates the wepaons info table setup above... [Could do this without a separate template
       but this is small enough]
     ******************************************************************************************** -->

<xsl:template match="weapon">
  <TR>
    <TD>
      <xsl:value-of select="@name"/>
    </TD>
    <TD>
      <xsl:value-of select="@type"/>
    </TD>
    <TD>
      <xsl:value-of select="@range"/>
    </TD>
    <TD>
      <xsl:value-of select="@damage"/>
    </TD>
  </TR>
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description:
       Templates to output the Objectives descriptions and points...                              -->
<!-- ******************************************************************************************** -->
<xsl:template match="objectives">
    <h2>Objectives</h2>
    <p>The following lists the key objectives in this scenario:</p> 
    <ol>
      <xsl:apply-templates/>
    </ol>
</xsl:template>

<xsl:template match="objective">
      <li><b><xsl:value-of select="@name"/>, <xsl:value-of select="@points"/> pts, <xsl:value-of select="@owner"/>: </b> <xsl:value-of select="."/></li>
</xsl:template>

<!-- ******************************************************************************************** -->
<!-- Description:
       Misc templates to suppress the output of stuff that's been directly stolen ;-) Bit lame... -->
<!-- ******************************************************************************************** -->

<xsl:template match="name"/>
<xsl:template match="turns"/>
<xsl:template match="location"/>
<xsl:template match="date"/>
<xsl:template match="description"/>

<!-- ******************************************************************************************** -->
     </xsl:stylesheet>
<!-- ******************************************************************************************** -->
