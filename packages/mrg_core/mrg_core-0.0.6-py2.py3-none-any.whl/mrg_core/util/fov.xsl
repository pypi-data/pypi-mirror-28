<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="xmfLogin.xml"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:mf="urn:schemas-microsoft-com:xslt"
  exclude-result-prefixes="mf"
>
<!--
  <xsl:output method="xml" version="1.0" indent="yes" encoding="UTF-8"/>
-->
<!--
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"

    doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN"
    doctype-system="http://www.w3.org/TR/html4/loose.dtd"
-->
	<xsl:output method="html" version="4.0" encoding="UTF-8" indent="yes"
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
	/>

  <xsl:variable name="hours">
    <node value="12">12</node>
    <node value="13">13</node>
    <node value="14">14</node>
    <node value="15">15</node>
    <node value="16">16</node>
    <node value="17">17</node>
    <node value="18">18</node>
    <node value="19">19</node>
    <node value="20">20</node>
    <node value="21">21</node>
    <node value="22">22</node>
    <node value="23">23</node>
    <node value="00">00</node>
    <node value="01">01</node>
    <node value="02">02</node>
    <node value="03">03</node>
    <node value="04">04</node>
    <node value="05">05</node>
    <node value="06">06</node>
    <node value="07">07</node>
    <node value="08">08</node>
    <node value="09">09</node>
    <node value="10">10</node>
    <node value="11">11</node>
  </xsl:variable>
	<xsl:variable name="hoursNodeSet" select="document('')//xsl:variable[@name='hours']/node"/>

  <xsl:variable name="months">
    <node value="01">January</node>
    <node value="02">Febuary</node>
    <node value="03">March</node>
    <node value="04">April</node>
    <node value="05">May</node>
    <node value="06">June</node>
    <node value="07">July</node>
    <node value="08">August</node>
    <node value="09">September</node>
    <node value="10">October</node>
    <node value="11">November</node>
    <node value="12">December</node>
  </xsl:variable>
	<xsl:variable name="monthsNodeSet" select="document('')//xsl:variable[@name='months']/node"/>


	<!-- ================================ -->
  <xsl:template match="/">

<html>
<head>
<style>
input[type=text] {
	width:90%;
}
body {
	font-family:arial;
}

table {
	font-family:arial;
}

.params {
	border-collapse:collapse;
	font-size:12px;
}
.params th {
	text-align:left;
	background-color:#efefef;
	border:1px solid gray;
	padding:3px;
}
.params td {
	border:1px solid gray;
	padding:3px;
}

.grid2 {
	border-collapse:collapse;
	table-layout:fixed;
	empty-cells:show;
	height:20px;
	font-size:9px;
	width:1025px;
}

th {
	text-align:left;
}

.grid2 .date th {
	width:40px;
	text-align:left;
	font-size:9px;
	border-bottom:1px solid gray;
}
.grid2 td {
	border:none;
	border-left:1px solid gray;
	border-bottom:1px solid gray;
	width:40px;
}

.grid2 td div {
	background-color:red;
	width:100%;
	height:100%;
}

.month {
	background-color:lightgrey;
	white-space:nowrap;
	height:20px;
	font-weight:bold;
	font-size:16px;
	text-align:center;
}
.dateHead {
	background-color:lightgrey;
	white-space:nowrap;
	text-align:left;
}
.Sun {
	position:absolute;
	background-color:green;
	height:12px;
	font-size:9px;
	width:100px;
	z-index:-99;
	margin-top:-11px;
}

.Moon {
	position:absolute;
	background-color:#FF5930;
	height:12px;
	font-size:9px;
	width:100px;
	z-index:-99;
	margin-top:-11px;
}

.date {
	vertical-align:top;
}
tr.date:hover {
	background-color:pink;
	opacity:0.8;
}

.tip {
	position:absolute;
	left:50px;
	background-color:lightyellow;
	width:150px;
	display:none;
	border:1px solid black;
	padding:5px;
	font-size:12px;
	opacity:1.0;
	z-index:99;
	margin:10px;
}
</style>
<script>
	self.curTip = null;
	//-------------------------
	function nop() {}
	//-------------------------
	function toggleDetails(tr, isVisible) {
		var tip = tr.getElementsByTagName('span')[0];
		if (self.curTip) {
			self.curTip.style.display = 'none';
		}
		tip.style.display = isVisible ? 'block' : 'none';
		self.curTip = tip;
	}

</script>
</head>


<body>

<h1>MRG <xsl:value-of select="//param[@name='Camera']/@value"/> : Observation Schedule</h1>

<table class="params" width="1000" border="0" cellpadding="0" cellspacing="0">
<tr>
<th colspan="3" style="background-color:gray;color:white;">Input arguments used for processing</th>
</tr>
<tr>
	<th style="background-color:lightgrey;width:200px;">Key</th>
	<th style="background-color:lightgrey;width:200px;">Value</th>
	<th style="background-color:lightgrey;width:600px;">Description</th>
</tr>

<xsl:for-each select="//param">
	<xsl:if test="@name='SunSet'">
		<tr>
		<th colspan="3" style="background-color:gray;color:white;">Calculated Parameters</th>
		</tr>
	</xsl:if>
	<tr>
		<th><xsl:value-of select="@name"/></th>
		<td><xsl:value-of select="@value"/></td>
		<td><xsl:value-of select="."/></td>
	</tr>
</xsl:for-each>

<tr>
	<th colspan="3" style="background-color:gray;color:white;">Legend</th>
</tr>
<tr>
	<th>Night time observation</th>
	<td><div class="Sun" style="margin-top:-7px;border:1px solid black"/></td>
	<td>The period in which the sun is below the horizon and observation takes place (below the Horizon parameter)</td>
</tr>
<tr>
	<th>Moon close to FOV</th>
	<td><div class="Moon" style="margin-top:-7px;border:1px solid black"/></td>
	<td>The period where the Moon has it's closest approach to the FOV (less than the MinLunarAngle parameter)</td>
</tr>

</table>

<br/>
<br/>
<table class="grid2" border="0" style="border:1px gray solid;" cellpadding="0" cellspacing="0">

<xsl:for-each select="//date">

	<xsl:variable name="date" select="."/>

	<xsl:if test="$date/@date = '01'">
		<xsl:call-template name="genHeading">
			<xsl:with-param name="date" select="$date/@id"/>
		</xsl:call-template>
	</xsl:if>

<tr class="date" onmouseover="toggleDetails(this,true)" onmouseout="toggleDetails(this,false)">
	<th class="dateHead">
		<xsl:call-template name="genData"/>
	</th>

	<td></td><td></td><td></td><td></td><td></td><td></td>
	<td></td><td></td><td></td><td></td><td></td><td></td>
	<td></td><td></td><td></td><td></td><td></td><td></td>
	<td></td><td></td><td></td><td></td><td></td><td></td>

</tr>
</xsl:for-each>

</table>
</body>

</html>

	</xsl:template>

	<!-- ================================ -->
	<xsl:template name="genHeading">
		<xsl:param name="date"/>
		<tr>
			<th class="month" colspan="25" nowrap="1">
				<xsl:variable name="year" select="substring($date,1,4)"/>
				<xsl:variable name="month" select="substring($date,6,2)"/>
<!--
				<xsl:value-of select="$date"/>
-->
				<xsl:text> </xsl:text>
				<xsl:value-of select="$monthsNodeSet[@value=$month]"/>
				<xsl:text> </xsl:text>
				<xsl:value-of select="$year"/>
			</th>
		</tr>
		<tr>
			<th class="dateHead">date/HH</th>
			<xsl:for-each select="$hoursNodeSet">
				<th class="dateHead"><xsl:value-of select="."/></th>
			</xsl:for-each>
		</tr>

	</xsl:template>

	<!-- ================================ -->
	<xsl:template name="genData">
		<xsl:param name="date" select="."/>

		<xsl:variable name="evts" select="$date/event"/>
		<xsl:variable name="cnt" select="count($evts)"/>

		<xsl:variable name="lunNM">
			<xsl:choose>
				<xsl:when test="count($evts)=3 and $evts[2]/@state='True'">
					<xsl:text>12</xsl:text>
				</xsl:when>
				<xsl:when test="count($evts)=4 and $evts[2]/@state='True'">
					<xsl:text>32</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>23</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="lun0" select="$evts[number(substring($lunNM,1,1))]"/>
		<xsl:variable name="lun1" select="$evts[number(substring($lunNM,2,1))]"/>
		<xsl:variable name="sun0" select="$evts[1]"/>
		<xsl:variable name="sun1" select="$evts[$cnt]"/>

		<xsl:variable name="title1">
			<xsl:text> Night: </xsl:text><xsl:value-of select="concat($sun0/@hh,':',$sun0/@mm,' - ',$sun1/@hh,':',$sun1/@mm)"/>
		</xsl:variable>
		<xsl:variable name="title2">
		<xsl:if test="$cnt>=3">
			<xsl:text>Moon: </xsl:text><xsl:value-of select="concat($lun0/@hh,':',$lun0/@mm,' - ',$lun1/@hh,':',$lun1/@mm)"/>
		</xsl:if>
		</xsl:variable>

		<xsl:value-of select="@date"/>

		<xsl:call-template name="genSchedule">
			<xsl:with-param name="class" select="'Sun'"/>
			<xsl:with-param name="sched0" select="$sun0"/>
			<xsl:with-param name="sched1" select="$sun1"/>
		</xsl:call-template>


		<xsl:if test="$cnt>=3">
			<xsl:call-template name="genSchedule">
				<xsl:with-param name="class" select="'Moon'"/>
				<xsl:with-param name="sched0" select="$lun0"/>
				<xsl:with-param name="sched1" select="$lun1"/>
			</xsl:call-template>
		</xsl:if>

		<span class="tip">
			<xsl:value-of select="$date/@id"/><br/>
			<xsl:value-of select="$title1"/><br/>
			<xsl:value-of select="$title2"/>
		</span>


	</xsl:template>

	<!-- ================================ -->
	<xsl:template name="genSchedule">
		<xsl:param name="class"/>
		<xsl:param name="sched0"/>
		<xsl:param name="sched1"/>

		<xsl:variable name="offsetHours">
			<xsl:choose>
				<xsl:when test="12.0 > number($sched0/@hh)">
					<xsl:value-of select="24.0"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="0.0"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="offsetDay">
			<xsl:choose>
				<xsl:when test="(number($sched0/@hh) - number($sched1/@hh)) > 0">
					<xsl:value-of select="12.0"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="-12.0"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="s0" select="number($sched0/@hh) + number($sched0/@mm) div 60 - 12 + number($offsetHours)"/>
		<xsl:variable name="s1" select="number($sched1/@hh) + number($sched1/@mm) div 60 + number($offsetDay) + number($offsetHours)"/>

		<xsl:variable name="xs0" select="round($s0*39+($s0)*2+48)"/>
		<xsl:variable name="xs1" select="round($s1*39+($s1)*2+48)"/>
		<xsl:variable name="ws" select="($xs1)-($xs0)"/>

		<div
			class="{$class}"
			setH="{$sched0/@hh}" setM="{$sched0/@mm}"
			riseH="{$sched1/@hh}" riseM="{$sched1/@mm}"
			style="left:{$xs0}px;width:{$ws}px;"
		>
<!--
		<xsl:value-of select="$ws"/>,
		<xsl:value-of select="$xs0"/>,
		<xsl:value-of select="$xs1"/>,
		<xsl:value-of select="$s0"/>,
		<xsl:value-of select="$s1"/>,
		<xsl:value-of select="$sched0/@hh"/>,
		<xsl:value-of select="$sched1/@hh"/>,
		<xsl:value-of select="$sched0/@mm"/>,
		<xsl:value-of select="$sched1/@mm"/>,
		<xsl:value-of select="$sched1/@offsetDay"/>,
		<xsl:value-of select="$sched1/@offsetHours"/>
-->
		</div>

	</xsl:template>


</xsl:stylesheet>