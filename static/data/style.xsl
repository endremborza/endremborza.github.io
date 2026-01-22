<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <title>Ideator</title>
        <link rel="stylesheet" href="styles.css" />
      </head>
      <body>
        <h2>Interests</h2>
        <div class="grid">
          <xsl:for-each select="root/interests/interest">
            <div class="card">
              <h3>
                <xsl:value-of select="title" />
              </h3>
              <div class="desc">
                <xsl:value-of select="description" />
              </div>
            </div>
          </xsl:for-each>
        </div>
        <xsl:for-each select="root/formats/format">
          <xsl:variable name="formatId" select="@id" />
          <h2>
            <xsl:value-of select="name" />
          </h2>
          <div class="grid">
            <xsl:for-each select="/root/ideas/idea[@format = $formatId]">
              <div class="card">
                <h3>
                  <xsl:value-of select="title" />
                </h3>

                <xsl:if test="description">
                  <div class="desc">
                    <xsl:value-of select="description" />
                  </div>
                </xsl:if>
                <xsl:if test="parent">
                  <div class="parent-ref">↳ Child of: <xsl:value-of select="parent" /></div>
                </xsl:if>
              </div>
            </xsl:for-each>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
