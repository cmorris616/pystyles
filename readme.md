# PyStyles

**_This library is still under construction and is not ready for use_**

PyStyles can be used to retrieve the styles for an element from an HTML document. This library uses BeautifulSoup for
reading the HTML and applies custom processes for reading the styles from the `style` tag. The styles are then applied
to the HTML tags adhering to the CSS processing rules. Styles with higher precedence will overwrite styles with lower
precedence. This results in the inability to determine if certain styles were ever applied to a particular tag.

