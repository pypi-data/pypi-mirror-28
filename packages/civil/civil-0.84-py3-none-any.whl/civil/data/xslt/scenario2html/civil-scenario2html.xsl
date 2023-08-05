<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!-- ******************************************************************************************** -->
<!-- Description :    Template for the transformation of Civil Scenarios to [X]HTML for web       -->
<!--             |    based display. Expected to form part of the documentation for a given game  -->
<!--             |    as players can swap the HTML versions, and the server can retreive the real -->
<!--             |    XML scenario from our repository...                                         -->
<!--                                                                                              -->
<!-- Author      :    Gareth Noyce                                                                -->
<!--                                                                                              -->
<!-- Version     :    0.1                                                                         -->
<!--                                                                                              -->
<!-- History     :    0.1 - (25/07/01) - Initial version just to start outputting content...      -->
<!--             |        - (09/10/01) - Changed the layout to match that of the website...       -->
<!--                                                                                              -->
<!-- Notes       :    There's currently no namespace declared for Civil scenarios. This is 
                 |    something that I should really fix just for peace of mind. Probably affects
                 |    the code considerably, so I'll leave it for now...                          -->
<!-- ******************************************************************************************** -->

<xsl:output method="html"/>

<!-- ******************************************************************************************** -->
<!-- Module Import Declarations...                                                                -->
<!--   These modules do all the real work. See each file for comments...                          -->
<!-- ******************************************************************************************** -->

<xsl:include href="../modules/mod-civil-headElement.xsl"/> 
<xsl:include href="../modules/mod-civil-scenarioInfo.xsl"/> 
<xsl:include href="../modules/mod-civil-colourVar.xsl"/>
<xsl:include href="../modules/mod-civil-generateMapPreview.xsl"/>
<xsl:include href="../modules/mod-civil-leaderInfo.xsl"/>

<!-- ******************************************************************************************** -->
<!-- Description :                                                                                -->
<!--       Base template, matches the root of the imcoming stream and sets-up the HTML document,  -->
<!--       it's style sheet and any other misc info...                                            -->
<!-- Notes:                                                                                       -->
<!--       Uses modules imported above and explicitly calls the templates required. See module's  -->
<!--       source for comments and further description...                                         -->
<!-- ******************************************************************************************** -->

<xsl:template match="/">
    <html>
      <xsl:call-template name="mod-civil-headElement"/>
      <BODY BGCOLOR="#312020" TEXT="#000000" LINK="#993300" ALINK="#990000">
      <DIV ALIGN="CENTER" STYLE="margin-top: 24pt;">
        <IMG SRC="../images/web-logo.jpg" ALT="Civil - American  Civil WarGaming" BORDER="0" WIDTH="307" HEIGHT="142" STYLE="margin-bottom: 24pt;"/>
        <TABLE BORDER="0" CELLPADDING="0" CELLSPACING="0" WIDTH="780"> 
	        <TR> 
                <TD BGCOLOR="#000000" WIDTH="8" HEIGHT="8"><IMG SRC="../images/dialog-widgetFrm-topleft.jpg" WIDTH="8" HEIGHT="8" BORDER="0"/></TD>
                <TD BGCOLOR="#000000" HEIGHT="8" BACKGROUND="../images/dialog-widgetFrm-top.jpg"><IMG SRC="../images/dialog-widgetFrm-top.jpg" WIDTH="72" HEIGHT="8" BORDER="0"/></TD> 
					 <TD BGCOLOR="#000000" WIDTH="8" HEIGHT="8"
					  BACKGROUND="../images/dialog-widgetFrm-topright.jpg"><IMG
						SRC="../images/dialog-widgetFrm-topright.jpg" WIDTH="8" HEIGHT="8"
                                         BORDER="0"/></TD> 
				  </TR> 
				  <TR> 
					 <TD BGCOLOR="#000000" WIDTH="8"
					  BACKGROUND="../images/dialog-widgetFrm-left.jpg"><IMG
                                         SRC="../images/dialog-widgetFrm-left.jpg" WIDTH="8" HEIGHT="72" BORDER="0"/></TD> 
					 <TD BGCOLOR="#FFFFFF"> 
                                        
                                                <xsl:apply-templates/>
                                        
                                        </TD> 
					 <TD BGCOLOR="#000000"
					  BACKGROUND="../images/dialog-widgetFrm-right.jpg" WIDTH="8"><IMG
                                         SRC="../images/dialog-widgetFrm-right.jpg" WIDTH="8" HEIGHT="72" BORDER="0"/></TD> 
				  </TR> 
				  <TR> 
					 <TD BGCOLOR="#000000" HEIGHT="8" WIDTH="8"><IMG
                                         SRC="../images/dialog-widgetFrm-botleft.jpg" WIDTH="8" HEIGHT="8" BORDER="0"/></TD>
					 
					 <TD BGCOLOR="#000000"
					  BACKGROUND="../images/dialog-widgetFrm-bot.jpg" HEIGHT="8"><IMG
                                         SRC="../images/dialog-widgetFrm-bot.jpg" WIDTH="72" HEIGHT="8" BORDER="0"/></TD> 
					 <TD BGCOLOR="#000000" WIDTH="8" HEIGHT="8"><IMG
						SRC="../images/dialog-widgetFrm-botright.jpg" WIDTH="8" HEIGHT="8"
                                         BORDER="0"/></TD> 
				  </TR>  
                                </TABLE><P>This HTML has been automatically generated with the civil-scenario2html.xsl stylesheet.</P></DIV> 
      </BODY>
    </html>
  </xsl:template>

<!-- ******************************************************************************************** -->
     </xsl:stylesheet>
<!-- ******************************************************************************************** -->






