# A
""""""
"""
Input
NLP:
    - Sentiment analysis
        > positive
        > negative
        > neutral
    - Parts of Speech
    - Important/Frequently-Occurring Words
"""

# A -> B
"""
Use data from the significant sentences given from the text processed
in A and send keywords to the web scraper for Google image searching.
"""

# B
"""
Web Scraping
    - Google Image Search using keywords from A
    - Download images
"""

# B -> C
"""
Take the image results from B and transform them using computer vision
tools in C.
"""

# C
"""
Computer Vision
    - Image Collage
        > Read in downloaded images from B
        > Find object contours and clip out
        > Piece back together on large background (search for
          using the "most important" word in the text)
"""

# C -> D
"""
Send the processed and transformed visual data back to the user.
"""

# D
"""
Output
"""
